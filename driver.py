import logging
import argparse
import asyncio
import glob
import math
from threading import Lock

import grpc
from google.protobuf.empty_pb2 import Empty

import driver_service_pb2_grpc as services
from driver_service_pb2 import HelloRequest, HelloResponse, TaskInfo, TaskType


class AtomicInt:

    def __init__(self, value: int = 0):
        self.value = value
        self._lock = Lock()

    def __iadd__(self, other: int):
        with self._lock:
            self.value += other
        return self

    def add_get_value(self, other: int) -> int:
        with self._lock:
            self.value += other
            return self.value

    def __lt__(self, other: float):
        return self.value < other

    def __eq__(self, other: int):
        return self.value == other

class AtomicState:

    def __init__(self, value = TaskType.Map):
        self._value = value
        self._lock = Lock()

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, value):
        with self._lock:
            self._value = value 


class DriverService(services.DriverServiceServicer):

    def __init__(self, N: int, M: int):
        self._N = N
        self._M = M
        self._input_files = glob.glob('inputs/*')
        self._files_per_map = int(math.ceil(len(self._input_files) / N))
        self._state = AtomicState()
        self._task_id = AtomicInt()
        self._finished_counter = AtomicInt()

    async def SayHello(self, request: HelloRequest, context: grpc.aio.ServicerContext) -> HelloResponse:
        return HelloResponse(message=f'Hello {request.name}')

    async def AskTask(self, request: Empty, context: grpc.aio.ServicerContext) -> TaskInfo:
        if self._state.value == TaskType.Map:
            task_id = self._task_id.add_get_value(1) - 1
            if task_id == self._N - 1:
                self._state.value = TaskType.NoOp

            logging.info('starting map %d', task_id)

            filenames = self._input_files[task_id*self._files_per_map:(task_id+1)*self._files_per_map]
            return TaskInfo(type=TaskType.Map, id=task_id, filenames=filenames, M=self._M)

        if self._state.value == TaskType.Reduce:
            task_id = self._task_id.add_get_value(1) - 1
            if task_id == self._M - 1:
                self._state.value = TaskType.NoOp

            logging.info('starting reduce %d', task_id)

            return TaskInfo(type=TaskType.Reduce, id=task_id)

        return TaskInfo(type=TaskType.NoOp, id=0)

    async def FinishMap(self, request: Empty, context: grpc.aio.ServicerContext) -> Empty:
        finished = self._finished_counter.add_get_value(1)
        if finished == self._N:
            self._state.value = TaskType.Reduce
            self._task_id = AtomicInt()
            self._finished_counter = AtomicInt()
        return Empty()

    async def FinishReduce(self, request: Empty, context: grpc.aio.ServicerContext) -> Empty:
        finished = self._finished_counter.add_get_value(1)
        if finished == self._M:
            logging.info('finished!')
        return Empty()


async def serve(service: DriverService) -> None:
    server = grpc.aio.server()
    services.add_DriverServiceServicer_to_server(service, server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
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
