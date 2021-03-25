import time
import logging
import asyncio
import grpc

from driver_service_pb2_grpc import DriverServiceStub
from driver_service_pb2 import HelloRequest


async def run() -> None:
    available = True
    while True:
        try:
            async with grpc.aio.insecure_channel('localhost:50051') as channel:
                stub = DriverServiceStub(channel)
                response = await stub.SayHello(HelloRequest(name='you'))
                available = True
            print("Greeter client received: " + response.message)
        except grpc.aio._call.AioRpcError as e:
            if not e._code == grpc.StatusCode.UNAVAILABLE:
                raise
            if available:
                logging.info('driver is unavailable')
            available = False
            time.sleep(1)
            


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
