import logging
from typing import List, Dict, IO

import grpc
from google.protobuf.empty_pb2 import Empty

from driver_service_pb2_grpc import DriverServiceStub


INTERMEDIATE_DIR = 'intermediate'
SERVER_ADDRESS = 'localhost:50051'


class FileCache:
    r'''
    Stores a set of files and closes them at the end
    '''

    def __init__(self, filemode: str = 'a'):
        self._filemode = filemode
        self._files: Dict[str, IO] = {}
        self._is_entered = False

    def get_file(self, filename: str) -> IO:
        r'''
        Opens the file in append mode if it's not already
        opened, and returns the file
        '''
        assert self._is_entered, "First, enter file cache using with statement"

        if filename not in self._files:
            self._files[filename] = open(filename, self._filemode)
        return self._files[filename]

    def __enter__(self):
        assert not self._is_entered, "You cannot enter file cache when already is entered"
        self._is_entered = True
        self._files: Dict[str, IO] = {}

    def __exit__(self, exception_type, exception_value, traceback):
        self._is_entered = False
        for file in self._files.values():
            file.close()


class Mapper:
    r'''
    Performs the map task
    '''
    def __init__(self):
        self._file_cache = FileCache()

    def _map_file(self, map_id: int, filename: str, M: int) -> None:
        r'''
        Maps given file into buckets
        '''
        with open(filename, 'r') as file:
            logging.info('mapping file %s', filename)
            text :str = file.read()
            for word in text.split():
                bucket_id = ord(word[0]) % M
                bf = self._file_cache.get_file(f'{INTERMEDIATE_DIR}/mr-{map_id}-{bucket_id}')
                bf.write(f'{word}\n')

    async def _finish_map(self) -> None:
        r'''
        Calls FinishMap rpc
        '''
        async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
            stub = DriverServiceStub(channel)
            await stub.FinishMap(Empty())

    async def map(self, map_id: int, filenames: List[str], M: int) -> None:
        r'''
        Map task
        '''
        logging.info('starting map %d', map_id)
        with self._file_cache:
            for filename in filenames:
                self._map_file(map_id, filename, M)
        await self._finish_map()
