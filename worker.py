import time
from typing import List, Dict, Tuple, Any
import logging
import asyncio
import glob
from enum import Enum

import grpc
from google.protobuf.empty_pb2 import Empty
from aiofiles import open as async_open
from aiofiles.base import AiofilesContextManager

from driver_service_pb2_grpc import DriverServiceStub
from driver_service_pb2 import HelloRequest, TaskType, TaskInfo


class WorkerState(Enum):
    Waiting = 0
    Idle = 1
    Working = 2


class FileCache:

    def __init__(self):
        self._files: Dict[str: AiofilesContextManager] = {}

    async def get_file(self, filename: str) -> AiofilesContextManager:
        if filename not in self._files:
            self._files[filename] = await async_open(filename, 'a')
        return self._files[filename]

    async def __aenter__(self):
        self._files: Dict[str: AiofilesContextManager] = {}

    async def __aexit__(self, exception_type, exception_value, traceback):
        for file in self._files.values():
            await file.close()


class WordCounter:

    def __init__(self):
        self._dict: Dict[str, int] = {}

    def count(self, word: int) -> None:
        if word not in self._dict:
            self._dict[word] = 0
        self._dict[word] += 1

    def items(self) -> List[Tuple[str, int]]:
        return self._dict.items()


class Worker:

    def __init__(self):
        self._state = WorkerState.Working
        self._file_cache = FileCache()
    
    def _noop(self):
        if self._state != WorkerState.Idle:
            logging.info('idle')

    async def _map(self, map_id: int, filenames: List[str], M: int) -> None:
        logging.info('starting map %d', map_id)
        async with self._file_cache:
            for filename in filenames:
                async with async_open(filename, 'r') as file:
                    logging.info('mapping file %s', filename)
                    text :str = await file.read()
                    for word in text.split():
                        bucket_id = ord(word[0]) % M
                        bf = await self._file_cache.get_file(f'intermediate/mr-{map_id}-{bucket_id}')
                        await bf.write(f'{word}\n')
        await self._finish_map()

    async def _reduce(self, bucket_id: int) -> None:
        logging.info('starting reduce %d', bucket_id)
        wc = WordCounter()
        for bucket_file in glob.glob(f'intermediate/mr-*-{bucket_id}'):
            async with async_open(bucket_file) as bf:
                async for word in bf:
                    wc.count(word)

        async with async_open(f'out/out-{bucket_id}', 'a') as out:
            for word, count in wc.items():
                await out.write(f'{word[:-1]} {count}\n')
        await self._finish_reduce()

    async def _ask_task(self) -> TaskInfo:
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = DriverServiceStub(channel)
            task = await stub.AskTask(Empty())
        return task

    async def _finish_map(self) -> None:
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = DriverServiceStub(channel)
            await stub.FinishMap(Empty())

    async def _finish_reduce(self) -> None:
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = DriverServiceStub(channel)
            await stub.FinishReduce(Empty())

    def _handle_rpc_error(self, e: grpc.aio._call.AioRpcError) -> bool:
        if not e._code == grpc.StatusCode.UNAVAILABLE:
            return False
        if self._state != WorkerState.Waiting:
            logging.info('driver is unavailable')
        self._state = WorkerState.Waiting
        time.sleep(1)
        return True

    async def run(self) -> None:
        while True:
            try:
                task = await self._ask_task()
                if task.type == TaskType.Map:
                    self._state = WorkerState.Working
                    await self._map(task.id, task.filenames, task.M)
                elif task.type == TaskType.Reduce:
                    self._state = WorkerState.Working
                    await self._reduce(task.id)
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
