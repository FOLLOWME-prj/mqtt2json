
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='opencensus/proto/agent/common/v1/common.proto',
  package='opencensus.proto.agent.common.v1',
  syntax='proto3',
  serialized_options=b'\n#io.opencensus.proto.agent.common.v1B\013CommonProtoP\001ZIgithub.com/census-instrumentation/opencensus-proto/gen-go/agent/common/v1\352\002$OpenCensus::Proto::Agent::Common::V1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-opencensus/proto/agent/common/v1/common.proto\x12 opencensus.proto.agent.common.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd8\x02\n\x04Node\x12G\n\nidentifier\x18\x01 \x01(\x0b\x32\x33.opencensus.proto.agent.common.v1.ProcessIdentifier\x12\x43\n\x0clibrary_info\x18\x02 \x01(\x0b\x32-.opencensus.proto.agent.common.v1.LibraryInfo\x12\x43\n\x0cservice_info\x18\x03 \x01(\x0b\x32-.opencensus.proto.agent.common.v1.ServiceInfo\x12J\n\nattributes\x18\x04 \x03(\x0b\x32\x36.opencensus.proto.agent.common.v1.Node.AttributesEntry\x1a\x31\n\x0f\x41ttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"h\n\x11ProcessIdentifier\x12\x11\n\thost_name\x18\x01 \x01(\t\x12\x0b\n\x03pid\x18\x02 \x01(\r\x12\x33\n\x0fstart_timestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xa7\x02\n\x0bLibraryInfo\x12H\n\x08language\x18\x01 \x01(\x0e\x32\x36.opencensus.proto.agent.common.v1.LibraryInfo.Language\x12\x18\n\x10\x65xporter_version\x18\x02 \x01(\t\x12\x1c\n\x14\x63ore_library_version\x18\x03 \x01(\t\"\x95\x01\n\x08Language\x12\x18\n\x14LANGUAGE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x43PP\x10\x01\x12\x0b\n\x07\x43_SHARP\x10\x02\x12\n\n\x06\x45RLANG\x10\x03\x12\x0b\n\x07GO_LANG\x10\x04\x12\x08\n\x04JAVA\x10\x05\x12\x0b\n\x07NODE_JS\x10\x06\x12\x07\n\x03PHP\x10\x07\x12\n\n\x06PYTHON\x10\x08\x12\x08\n\x04RUBY\x10\t\x12\n\n\x06WEB_JS\x10\n\"\x1b\n\x0bServiceInfo\x12\x0c\n\x04name\x18\x01 \x01(\tB\xa6\x01\n#io.opencensus.proto.agent.common.v1B\x0b\x43ommonProtoP\x01ZIgithub.com/census-instrumentation/opencensus-proto/gen-go/agent/common/v1\xea\x02$OpenCensus::Proto::Agent::Common::V1b\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_LIBRARYINFO_LANGUAGE = _descriptor.EnumDescriptor(
  name='Language',
  full_name='opencensus.proto.agent.common.v1.LibraryInfo.Language',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LANGUAGE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CPP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='C_SHARP', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERLANG', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GO_LANG', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='JAVA', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NODE_JS', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHP', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PYTHON', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RUBY', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WEB_JS', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=716,
  serialized_end=865,
)
_sym_db.RegisterEnumDescriptor(_LIBRARYINFO_LANGUAGE)


_NODE_ATTRIBUTESENTRY = _descriptor.Descriptor(
  name='AttributesEntry',
  full_name='opencensus.proto.agent.common.v1.Node.AttributesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='opencensus.proto.agent.common.v1.Node.AttributesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='opencensus.proto.agent.common.v1.Node.AttributesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=412,
  serialized_end=461,
)

_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='opencensus.proto.agent.common.v1.Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='opencensus.proto.agent.common.v1.Node.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='library_info', full_name='opencensus.proto.agent.common.v1.Node.library_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service_info', full_name='opencensus.proto.agent.common.v1.Node.service_info', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attributes', full_name='opencensus.proto.agent.common.v1.Node.attributes', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_NODE_ATTRIBUTESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=461,
)


_PROCESSIDENTIFIER = _descriptor.Descriptor(
  name='ProcessIdentifier',
  full_name='opencensus.proto.agent.common.v1.ProcessIdentifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='host_name', full_name='opencensus.proto.agent.common.v1.ProcessIdentifier.host_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pid', full_name='opencensus.proto.agent.common.v1.ProcessIdentifier.pid', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_timestamp', full_name='opencensus.proto.agent.common.v1.ProcessIdentifier.start_timestamp', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=463,
  serialized_end=567,
)


_LIBRARYINFO = _descriptor.Descriptor(
  name='LibraryInfo',
  full_name='opencensus.proto.agent.common.v1.LibraryInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='language', full_name='opencensus.proto.agent.common.v1.LibraryInfo.language', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exporter_version', full_name='opencensus.proto.agent.common.v1.LibraryInfo.exporter_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='core_library_version', full_name='opencensus.proto.agent.common.v1.LibraryInfo.core_library_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LIBRARYINFO_LANGUAGE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=570,
  serialized_end=865,
)


_SERVICEINFO = _descriptor.Descriptor(
  name='ServiceInfo',
  full_name='opencensus.proto.agent.common.v1.ServiceInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='opencensus.proto.agent.common.v1.ServiceInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=867,
  serialized_end=894,
)

_NODE_ATTRIBUTESENTRY.containing_type = _NODE
_NODE.fields_by_name['identifier'].message_type = _PROCESSIDENTIFIER
_NODE.fields_by_name['library_info'].message_type = _LIBRARYINFO
_NODE.fields_by_name['service_info'].message_type = _SERVICEINFO
_NODE.fields_by_name['attributes'].message_type = _NODE_ATTRIBUTESENTRY
_PROCESSIDENTIFIER.fields_by_name['start_timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LIBRARYINFO.fields_by_name['language'].enum_type = _LIBRARYINFO_LANGUAGE
_LIBRARYINFO_LANGUAGE.containing_type = _LIBRARYINFO
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['ProcessIdentifier'] = _PROCESSIDENTIFIER
DESCRIPTOR.message_types_by_name['LibraryInfo'] = _LIBRARYINFO
DESCRIPTOR.message_types_by_name['ServiceInfo'] = _SERVICEINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), {

  'AttributesEntry' : _reflection.GeneratedProtocolMessageType('AttributesEntry', (_message.Message,), {
    'DESCRIPTOR' : _NODE_ATTRIBUTESENTRY,
    '__module__' : 'opencensus.proto.agent.common.v1.common_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.agent.common.v1.Node.AttributesEntry)
    })
  ,
  'DESCRIPTOR' : _NODE,
  '__module__' : 'opencensus.proto.agent.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.agent.common.v1.Node)
  })
_sym_db.RegisterMessage(Node)
_sym_db.RegisterMessage(Node.AttributesEntry)

ProcessIdentifier = _reflection.GeneratedProtocolMessageType('ProcessIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _PROCESSIDENTIFIER,
  '__module__' : 'opencensus.proto.agent.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.agent.common.v1.ProcessIdentifier)
  })
_sym_db.RegisterMessage(ProcessIdentifier)

LibraryInfo = _reflection.GeneratedProtocolMessageType('LibraryInfo', (_message.Message,), {
  'DESCRIPTOR' : _LIBRARYINFO,
  '__module__' : 'opencensus.proto.agent.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.agent.common.v1.LibraryInfo)
  })
_sym_db.RegisterMessage(LibraryInfo)

ServiceInfo = _reflection.GeneratedProtocolMessageType('ServiceInfo', (_message.Message,), {
  'DESCRIPTOR' : _SERVICEINFO,
  '__module__' : 'opencensus.proto.agent.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.agent.common.v1.ServiceInfo)
  })
_sym_db.RegisterMessage(ServiceInfo)


DESCRIPTOR._options = None
_NODE_ATTRIBUTESENTRY._options = None
# @@protoc_insertion_point(module_scope)
