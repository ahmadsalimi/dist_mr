import logging
import argparse
import asyncio
import glob
import math
import time
from threading import Lock

import grpc
from google.protobuf.empty_pb2 import Empty

import driver_service_pb2_grpc as services
from driver_service_pb2 import HelloRequest, HelloResponse, TaskInfo, TaskType


class DriverService(services.DriverServiceServicer):

    def __init__(self, N: int, M: int):
        self._N = N
        self._M = M
        self._input_files = glob.glob('inputs/*')
        self._task_lock = Lock()
        self._files_per_map = int(math.ceil(len(self._input_files) / N))
        self._state = TaskType.Map
        self._task_id = 0
        self._finished_counter = 0
        self._start_time = 0

    async def SayHello(self, request: HelloRequest, context: grpc.aio.ServicerContext) -> HelloResponse:
        return HelloResponse(message=f'Hello {request.name}')

    async def AskTask(self, request: Empty, context: grpc.aio.ServicerContext) -> TaskInfo:
        with self._task_lock:
            if self._state == TaskType.Map:
                task_id = self._task_id
                self._task_id += 1

                if task_id == self._N - 1:
                    self._state = TaskType.NoOp

                if task_id == 0:
                    self._start_time = time.time()

                logging.info('starting map %d', task_id)

                filenames = self._input_files[task_id*self._files_per_map:(task_id+1)*self._files_per_map]
                return TaskInfo(type=TaskType.Map, id=task_id, filenames=filenames, M=self._M)

            if self._state == TaskType.Reduce:
                task_id = self._task_id
                self._task_id += 1

                if task_id == self._M - 1:
                    self._state = TaskType.NoOp

                logging.info('starting reduce %d', task_id)

                return TaskInfo(type=TaskType.Reduce, id=task_id)

            return TaskInfo(type=TaskType.NoOp, id=0)

    async def FinishMap(self, request: Empty, context: grpc.aio.ServicerContext) -> Empty:
        with self._task_lock:
            self._finished_counter += 1
            if self._finished_counter == self._N:
                self._state = TaskType.Reduce
                self._task_id = 0
                self._finished_counter = 0
            return Empty()

    async def FinishReduce(self, request: Empty, context: grpc.aio.ServicerContext) -> Empty:
        with self._task_lock:
            self._finished_counter += 1
            if self._finished_counter == self._M:
                logging.info('finished at %.4f secs!', time.time() - self._start_time)
            return Empty()


def create_server(service: DriverService) -> grpc.aio.Server:
    server = grpc.aio.server()
    services.add_DriverServiceServicer_to_server(service, server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    return server


async def serve(service: DriverService) -> None:
    server = create_server(service)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Starts the driver.')
    parser.add_argument('-N', dest='N', type=int, required=True, help='Number of Map tasks')
    parser.add_argument('-M', dest='M', type=int, required=True, help='Number of Reduce tasks')

    args = parser.parse_args()

    service = DriverService(args.N, args.M)

    asyncio.run(serve(service))
