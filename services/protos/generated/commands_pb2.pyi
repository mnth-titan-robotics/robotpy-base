import geometry2d_pb2 as _geometry2d_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuestNavCommandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMAND_TYPE_UNSPECIFIED: _ClassVar[QuestNavCommandType]
    POSE_RESET: _ClassVar[QuestNavCommandType]
COMMAND_TYPE_UNSPECIFIED: QuestNavCommandType
POSE_RESET: QuestNavCommandType

class ProtobufQuestNavPoseResetPayload(_message.Message):
    __slots__ = ("target_pose",)
    TARGET_POSE_FIELD_NUMBER: _ClassVar[int]
    target_pose: _geometry2d_pb2.ProtobufPose2d
    def __init__(self, target_pose: _Optional[_Union[_geometry2d_pb2.ProtobufPose2d, _Mapping]] = ...) -> None: ...

class ProtobufQuestNavCommand(_message.Message):
    __slots__ = ("type", "command_id", "pose_reset_payload")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    POSE_RESET_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    type: QuestNavCommandType
    command_id: int
    pose_reset_payload: ProtobufQuestNavPoseResetPayload
    def __init__(self, type: _Optional[_Union[QuestNavCommandType, str]] = ..., command_id: _Optional[int] = ..., pose_reset_payload: _Optional[_Union[ProtobufQuestNavPoseResetPayload, _Mapping]] = ...) -> None: ...

class ProtobufQuestNavCommandResponse(_message.Message):
    __slots__ = ("command_id", "success", "error_message")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    command_id: int
    success: bool
    error_message: str
    def __init__(self, command_id: _Optional[int] = ..., success: bool = ..., error_message: _Optional[str] = ...) -> None: ...
