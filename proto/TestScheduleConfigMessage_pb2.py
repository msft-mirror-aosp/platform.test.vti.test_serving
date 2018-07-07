# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vti/test_serving/proto/TestScheduleConfigMessage.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='vti/test_serving/proto/TestScheduleConfigMessage.proto',
  package='android.test.lab',
  syntax='proto2',
  serialized_pb=_b('\n6vti/test_serving/proto/TestScheduleConfigMessage.proto\x12\x10\x61ndroid.test.lab\"\xe4\x01\n\x15ScheduleConfigMessage\x12\x17\n\x0fmanifest_branch\x18\x01 \x01(\x0c\x12\x16\n\x0epab_account_id\x18\x02 \x01(\x0c\x12V\n\x12\x62uild_storage_type\x18\x03 \x01(\x0e\x32\".android.test.lab.BuildStorageType:\x16\x42UILD_STORAGE_TYPE_PAB\x12\x42\n\x0c\x62uild_target\x18\x0b \x03(\x0b\x32,.android.test.lab.BuildScheduleConfigMessage\"\xd2\x01\n\x1a\x42uildScheduleConfigMessage\x12\x0c\n\x04name\x18\x01 \x01(\x0c\x12#\n\x1brequire_signed_device_build\x18\x02 \x01(\x08\x12 \n\x12has_bootloader_img\x18\x03 \x01(\x08:\x04true\x12\x1b\n\rhas_radio_img\x18\x04 \x01(\x08:\x04true\x12\x42\n\rtest_schedule\x18\x0b \x03(\x0b\x32+.android.test.lab.TestScheduleConfigMessage\"\xe4\x05\n\x19TestScheduleConfigMessage\x12\x11\n\ttest_name\x18\x01 \x01(\x0c\x12\x0e\n\x06period\x18\x02 \x01(\x05\x12\x10\n\x08priority\x18\x03 \x01(\x0c\x12\x0e\n\x06\x64\x65vice\x18\x04 \x03(\x0c\x12\x0e\n\x06shards\x18\x05 \x01(\x05\x12\x1f\n\x17required_host_equipment\x18\x06 \x03(\x0c\x12!\n\x19required_device_equipment\x18\x07 \x03(\x0c\x12\r\n\x05param\x18\x0b \x01(\x0c\x12T\n\x10gsi_storage_type\x18\x18 \x01(\x0e\x32\".android.test.lab.BuildStorageType:\x16\x42UILD_STORAGE_TYPE_PAB\x12\x12\n\ngsi_branch\x18\x15 \x01(\x0c\x12\x18\n\x10gsi_build_target\x18\x16 \x01(\x0c\x12\x1a\n\x12gsi_pab_account_id\x18\x17 \x01(\x0c\x12\x1a\n\x12gsi_vendor_version\x18\x19 \x01(\x0c\x12U\n\x11test_storage_type\x18\" \x01(\x0e\x32\".android.test.lab.BuildStorageType:\x16\x42UILD_STORAGE_TYPE_PAB\x12\x13\n\x0btest_branch\x18\x1f \x01(\x0c\x12\x19\n\x11test_build_target\x18  \x01(\x0c\x12\x1b\n\x13test_pab_account_id\x18! \x01(\x0c\x12\x13\n\x0bretry_count\x18) \x01(\x05\x12\x16\n\x07\x64isable\x18\x33 \x01(\x08:\x05\x66\x61lse\x12\x1f\n\x17image_package_repo_base\x18= \x01(\x0c\x12\x15\n\rreport_bucket\x18G \x03(\x0c\x12\x1d\n\x15report_spreadsheet_id\x18H \x03(\x0c\x12\x1d\n\x15report_persistent_url\x18I \x03(\x0c\x12\x1c\n\x14report_reference_url\x18J \x03(\x0c*j\n\x10\x42uildStorageType\x12\x1e\n\x1aUNKNOWN_BUILD_STORAGE_TYPE\x10\x00\x12\x1a\n\x16\x42UILD_STORAGE_TYPE_PAB\x10\x01\x12\x1a\n\x16\x42UILD_STORAGE_TYPE_GCS\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_BUILDSTORAGETYPE = _descriptor.EnumDescriptor(
  name='BuildStorageType',
  full_name='android.test.lab.BuildStorageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_BUILD_STORAGE_TYPE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUILD_STORAGE_TYPE_PAB', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUILD_STORAGE_TYPE_GCS', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1263,
  serialized_end=1369,
)
_sym_db.RegisterEnumDescriptor(_BUILDSTORAGETYPE)

BuildStorageType = enum_type_wrapper.EnumTypeWrapper(_BUILDSTORAGETYPE)
UNKNOWN_BUILD_STORAGE_TYPE = 0
BUILD_STORAGE_TYPE_PAB = 1
BUILD_STORAGE_TYPE_GCS = 2



_SCHEDULECONFIGMESSAGE = _descriptor.Descriptor(
  name='ScheduleConfigMessage',
  full_name='android.test.lab.ScheduleConfigMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='manifest_branch', full_name='android.test.lab.ScheduleConfigMessage.manifest_branch', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pab_account_id', full_name='android.test.lab.ScheduleConfigMessage.pab_account_id', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_storage_type', full_name='android.test.lab.ScheduleConfigMessage.build_storage_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='android.test.lab.ScheduleConfigMessage.build_target', index=3,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=305,
)


_BUILDSCHEDULECONFIGMESSAGE = _descriptor.Descriptor(
  name='BuildScheduleConfigMessage',
  full_name='android.test.lab.BuildScheduleConfigMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='android.test.lab.BuildScheduleConfigMessage.name', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='require_signed_device_build', full_name='android.test.lab.BuildScheduleConfigMessage.require_signed_device_build', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='has_bootloader_img', full_name='android.test.lab.BuildScheduleConfigMessage.has_bootloader_img', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='has_radio_img', full_name='android.test.lab.BuildScheduleConfigMessage.has_radio_img', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_schedule', full_name='android.test.lab.BuildScheduleConfigMessage.test_schedule', index=4,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=308,
  serialized_end=518,
)


_TESTSCHEDULECONFIGMESSAGE = _descriptor.Descriptor(
  name='TestScheduleConfigMessage',
  full_name='android.test.lab.TestScheduleConfigMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_name', full_name='android.test.lab.TestScheduleConfigMessage.test_name', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='period', full_name='android.test.lab.TestScheduleConfigMessage.period', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='priority', full_name='android.test.lab.TestScheduleConfigMessage.priority', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device', full_name='android.test.lab.TestScheduleConfigMessage.device', index=3,
      number=4, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shards', full_name='android.test.lab.TestScheduleConfigMessage.shards', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='required_host_equipment', full_name='android.test.lab.TestScheduleConfigMessage.required_host_equipment', index=5,
      number=6, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='required_device_equipment', full_name='android.test.lab.TestScheduleConfigMessage.required_device_equipment', index=6,
      number=7, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='param', full_name='android.test.lab.TestScheduleConfigMessage.param', index=7,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gsi_storage_type', full_name='android.test.lab.TestScheduleConfigMessage.gsi_storage_type', index=8,
      number=24, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gsi_branch', full_name='android.test.lab.TestScheduleConfigMessage.gsi_branch', index=9,
      number=21, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gsi_build_target', full_name='android.test.lab.TestScheduleConfigMessage.gsi_build_target', index=10,
      number=22, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gsi_pab_account_id', full_name='android.test.lab.TestScheduleConfigMessage.gsi_pab_account_id', index=11,
      number=23, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gsi_vendor_version', full_name='android.test.lab.TestScheduleConfigMessage.gsi_vendor_version', index=12,
      number=25, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_storage_type', full_name='android.test.lab.TestScheduleConfigMessage.test_storage_type', index=13,
      number=34, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_branch', full_name='android.test.lab.TestScheduleConfigMessage.test_branch', index=14,
      number=31, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_build_target', full_name='android.test.lab.TestScheduleConfigMessage.test_build_target', index=15,
      number=32, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_pab_account_id', full_name='android.test.lab.TestScheduleConfigMessage.test_pab_account_id', index=16,
      number=33, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='retry_count', full_name='android.test.lab.TestScheduleConfigMessage.retry_count', index=17,
      number=41, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='disable', full_name='android.test.lab.TestScheduleConfigMessage.disable', index=18,
      number=51, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_package_repo_base', full_name='android.test.lab.TestScheduleConfigMessage.image_package_repo_base', index=19,
      number=61, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report_bucket', full_name='android.test.lab.TestScheduleConfigMessage.report_bucket', index=20,
      number=71, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report_spreadsheet_id', full_name='android.test.lab.TestScheduleConfigMessage.report_spreadsheet_id', index=21,
      number=72, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report_persistent_url', full_name='android.test.lab.TestScheduleConfigMessage.report_persistent_url', index=22,
      number=73, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='report_reference_url', full_name='android.test.lab.TestScheduleConfigMessage.report_reference_url', index=23,
      number=74, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=521,
  serialized_end=1261,
)

_SCHEDULECONFIGMESSAGE.fields_by_name['build_storage_type'].enum_type = _BUILDSTORAGETYPE
_SCHEDULECONFIGMESSAGE.fields_by_name['build_target'].message_type = _BUILDSCHEDULECONFIGMESSAGE
_BUILDSCHEDULECONFIGMESSAGE.fields_by_name['test_schedule'].message_type = _TESTSCHEDULECONFIGMESSAGE
_TESTSCHEDULECONFIGMESSAGE.fields_by_name['gsi_storage_type'].enum_type = _BUILDSTORAGETYPE
_TESTSCHEDULECONFIGMESSAGE.fields_by_name['test_storage_type'].enum_type = _BUILDSTORAGETYPE
DESCRIPTOR.message_types_by_name['ScheduleConfigMessage'] = _SCHEDULECONFIGMESSAGE
DESCRIPTOR.message_types_by_name['BuildScheduleConfigMessage'] = _BUILDSCHEDULECONFIGMESSAGE
DESCRIPTOR.message_types_by_name['TestScheduleConfigMessage'] = _TESTSCHEDULECONFIGMESSAGE
DESCRIPTOR.enum_types_by_name['BuildStorageType'] = _BUILDSTORAGETYPE

ScheduleConfigMessage = _reflection.GeneratedProtocolMessageType('ScheduleConfigMessage', (_message.Message,), dict(
  DESCRIPTOR = _SCHEDULECONFIGMESSAGE,
  __module__ = 'vti.test_serving.proto.TestScheduleConfigMessage_pb2'
  # @@protoc_insertion_point(class_scope:android.test.lab.ScheduleConfigMessage)
  ))
_sym_db.RegisterMessage(ScheduleConfigMessage)

BuildScheduleConfigMessage = _reflection.GeneratedProtocolMessageType('BuildScheduleConfigMessage', (_message.Message,), dict(
  DESCRIPTOR = _BUILDSCHEDULECONFIGMESSAGE,
  __module__ = 'vti.test_serving.proto.TestScheduleConfigMessage_pb2'
  # @@protoc_insertion_point(class_scope:android.test.lab.BuildScheduleConfigMessage)
  ))
_sym_db.RegisterMessage(BuildScheduleConfigMessage)

TestScheduleConfigMessage = _reflection.GeneratedProtocolMessageType('TestScheduleConfigMessage', (_message.Message,), dict(
  DESCRIPTOR = _TESTSCHEDULECONFIGMESSAGE,
  __module__ = 'vti.test_serving.proto.TestScheduleConfigMessage_pb2'
  # @@protoc_insertion_point(class_scope:android.test.lab.TestScheduleConfigMessage)
  ))
_sym_db.RegisterMessage(TestScheduleConfigMessage)


# @@protoc_insertion_point(module_scope)
