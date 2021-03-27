<div style="text-align: justify;">

# dist_mr

[![Build and Test](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml/badge.svg)](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml)


## GRPC API

### AskTask

Each idle worker, asks driver a task, and the driver decides to send one of the following responses:

- Map task: contains map id, file names to map and M
- Reduce task: contains reduce id (bucket id) to reduce intermediate files with given bucket id
- NoOp: tells to the worker to do nothing (Used when there's no map task left, but all map tasks are not finished and we cannot start reduce tasks)
- ShutDown: tells the worker to shut itself down

### FinishMap

When a worker finishes its map task, calls this rpc. This is important for driver to know when all map tasks are finished and start reduce tasks.

### FinishReduce

When a worker finishes its reduce task, calls this rpc. This is important for driver to know when all reduce tasks are finished and shut down the workers and itself.


Compile protobuf

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/driver-service.proto
```

</div>
