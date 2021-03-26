# dist_mr

[![Build and Test](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml/badge.svg)](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml)

Compile protobuf

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/driver-service.proto
```
