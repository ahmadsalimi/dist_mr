import logging
import asyncio
import grpc

import driver_service_pb2_grpc as services
from driver_service_pb2 import HelloRequest, HelloResponse


class DriverService(services.DriverServiceServicer):

    async def SayHello(self, request: HelloRequest, context: grpc.aio.ServicerContext) -> HelloResponse:
        return HelloResponse(message=f'Hello {request.name}')


async def serve() -> None:
    server = grpc.aio.server()
    services.add_DriverServiceServicer_to_server(DriverService(), server)
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
    asyncio.run(serve())
