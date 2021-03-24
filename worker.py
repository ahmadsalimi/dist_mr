import logging
import asyncio
import grpc

from driver_service_pb2_grpc import DriverServiceStub
from driver_service_pb2 import HelloRequest


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = DriverServiceStub(channel)
        response = await stub.SayHello(HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
