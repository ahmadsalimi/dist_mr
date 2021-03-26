import time
import logging
import asyncio
from enum import Enum

import grpc
from google.protobuf.empty_pb2 import Empty

from mapper import Mapper
from reducer import Reducer
from driver_service_pb2_grpc import DriverServiceStub
from driver_service_pb2 import TaskType, TaskInfo


SERVER_ADDRESS = 'localhost:50051'


class WorkerState(Enum):
    Waiting = 0     # Waiting for driver to start
    Idle = 1        # Given task is NoOp
    Working = 2     # Doing a Map or Reduce task


class Worker:

    def __init__(self):
        self._state = WorkerState.Working
        self._mapper = Mapper()
        self._reducer = Reducer()

    def _noop(self):
        r'''
        NoOp task
        '''
        # Just one time log idle
        if self._state != WorkerState.Idle:
            logging.info('idle')

    async def _ask_task(self) -> TaskInfo:
        r'''
        Calls AskTask rpc
        '''
        async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            task = await stub.AskTask(Empty())
        return task

    def _handle_rpc_error(self, e: grpc.aio._call.AioRpcError) -> bool:
        r'''
        Handles rpc Error in method call
        Returns False if error is not handled
        '''
        if not e._code == grpc.StatusCode.UNAVAILABLE:
            return False

        # Just one time log driver is unavailable
        if self._state != WorkerState.Waiting:
            logging.info('driver is unavailable')
            self._state = WorkerState.Waiting
        return True

    async def run(self) -> None:
        r'''
        Runs the worker and calls AskTask rpc forever
        '''
        while True:
            try:
                task = await self._ask_task()
                if task.type == TaskType.Map:
                    self._state = WorkerState.Working
                    await self._mapper.map(task.id, task.filenames, task.M)

                elif task.type == TaskType.Reduce:
                    self._state = WorkerState.Working
                    await self._reducer.reduce(task.id)

                else:
                    self._noop()
                    self._state = WorkerState.Idle
            except grpc.aio._call.AioRpcError as e:
                if not self._handle_rpc_error(e):
                    raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    worker = Worker()
    asyncio.run(worker.run())
