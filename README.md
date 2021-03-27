<div style="text-align: justify;">

# Distributed Map Reduce

A distributed map-reduce implemented by Python 3

[![Build and Test](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml/badge.svg)](https://github.com/ahmadsalimi/dist_mr/actions/workflows/main.yml)


## Install the dependencies

```bash
pip install -r requirements.txt
```

## Run a worker

Note: *Name is just used in the logging to identify each worker (That argument is optional)*

```bash
python worker.py [-h|--help] [--name NAME]
```

## Run the driver

```bash
python driver.py [-h|--help] -N N -M M
```

## Run the test

Note: *The tests also run in a Github Actions CI.*

```bash
pytest test.py
```

## GRPC API (`proto/driver-service.proto`)

### AskTask

Each idle worker, asks driver a task, and the driver decides to send one of the following responses:

- Map task: contains map id, file names to map and M
- Reduce task: contains reduce id (bucket id) to reduce intermediate files with given bucket id
- NoOp: tells to the worker to do nothing (Used when there's no map/reduce task left to assign, but all of them are not finished yet and we cannot switch to the next state)
- ShutDown: tells the worker to shut itself down

### FinishMap

When a worker finishes its map task, calls this rpc. This is important for driver to know when all map tasks are finished and start reduce tasks.

### FinishReduce

When a worker finishes its reduce task, calls this rpc. This is important for driver to know when all reduce tasks are finished and shut down the workers and itself.

You can compile the protobuf file using the following command:

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/driver-service.proto
```

## Driver (`driver.py`)

### Assign files to map tasks

The driver uses round robin algorithm to assign files to each map task.

### States of the driver

The state initially is set to `Map`. All the states change inside a lock and this changes are thread-safe.

1. Map: In this state, when a worker calls the `AskTask` rpc, assign the next `map_id` to the task and returns file names of that `map_id` to the worker.

1. Reduce: When all of the map tasks are finished, the driver switches to Reduce state. In this state, it returns the next reduce task id in the `AskTask` rpc.

1. NoOp: When there's no map (reduce) tasks left to assign, but all of them are not finished yet, the driver returns a NoOp task.

1. ShutDown: When all of the reduce tasks are finished, the driver switches to ShutDown state. In this state, it returns a ShutDown task.

## Worker (`worker.py`)

The workers wait for the driver to start. Then, they call the `AskTask` rpc in a loop and do the following according to the task type.

- Map: Uses the [Mapper](#Mapper) class to map the given input files into the intermediate files

- Reduce: Uses the [Reducer](#Reducer) class to reduce the given bucket id

- NoOp: The worker does nothing in this loop

- ShutDown: The worker shut itself down

### Mapper (`mapper.py`)

This class, splits the text of each given file using whitespaces, and adds each word to the corresponding bucket file.

### Reducer (`reducer.py`)

This class, counts each word of the given bucket id from intermediate files, and writes the result to the corresponding out file.

</div>
