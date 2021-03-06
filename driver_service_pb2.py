# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: driver-service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='driver-service.proto',
  package='dist_mr',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14\x64river-service.proto\x12\x07\x64ist_mr\x1a\x1bgoogle/protobuf/empty.proto\"U\n\x08TaskInfo\x12\x1f\n\x04type\x18\x01 \x01(\x0e\x32\x11.dist_mr.TaskType\x12\n\n\x02id\x18\x02 \x01(\r\x12\t\n\x01M\x18\x03 \x01(\r\x12\x11\n\tfilenames\x18\x04 \x03(\t*7\n\x08TaskType\x12\x07\n\x03Map\x10\x00\x12\n\n\x06Reduce\x10\x01\x12\x08\n\x04NoOp\x10\x02\x12\x0c\n\x08ShutDown\x10\x03\x32\xc8\x01\n\rDriverService\x12\x36\n\x07\x41skTask\x12\x16.google.protobuf.Empty\x1a\x11.dist_mr.TaskInfo\"\x00\x12=\n\tFinishMap\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12@\n\x0c\x46inishReduce\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])

_TASKTYPE = _descriptor.EnumDescriptor(
  name='TaskType',
  full_name='dist_mr.TaskType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Map', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Reduce', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NoOp', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ShutDown', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=149,
  serialized_end=204,
)
_sym_db.RegisterEnumDescriptor(_TASKTYPE)

TaskType = enum_type_wrapper.EnumTypeWrapper(_TASKTYPE)
Map = 0
Reduce = 1
NoOp = 2
ShutDown = 3



_TASKINFO = _descriptor.Descriptor(
  name='TaskInfo',
  full_name='dist_mr.TaskInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='dist_mr.TaskInfo.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='dist_mr.TaskInfo.id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='M', full_name='dist_mr.TaskInfo.M', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filenames', full_name='dist_mr.TaskInfo.filenames', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=147,
)

_TASKINFO.fields_by_name['type'].enum_type = _TASKTYPE
DESCRIPTOR.message_types_by_name['TaskInfo'] = _TASKINFO
DESCRIPTOR.enum_types_by_name['TaskType'] = _TASKTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskInfo = _reflection.GeneratedProtocolMessageType('TaskInfo', (_message.Message,), {
  'DESCRIPTOR' : _TASKINFO,
  '__module__' : 'driver_service_pb2'
  # @@protoc_insertion_point(class_scope:dist_mr.TaskInfo)
  })
_sym_db.RegisterMessage(TaskInfo)



_DRIVERSERVICE = _descriptor.ServiceDescriptor(
  name='DriverService',
  full_name='dist_mr.DriverService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=207,
  serialized_end=407,
  methods=[
  _descriptor.MethodDescriptor(
    name='AskTask',
    full_name='dist_mr.DriverService.AskTask',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_TASKINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FinishMap',
    full_name='dist_mr.DriverService.FinishMap',
    index=1,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FinishReduce',
    full_name='dist_mr.DriverService.FinishReduce',
    index=2,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DRIVERSERVICE)

DESCRIPTOR.services_by_name['DriverService'] = _DRIVERSERVICE

# @@protoc_insertion_point(module_scope)
