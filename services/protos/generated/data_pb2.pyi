import geometry3d_pb2 as _geometry3d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtobufQuestNavFrameData(_message.Message):
    __slots__ = ("frame_count", "timestamp", "pose3d")
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    POSE3D_FIELD_NUMBER: _ClassVar[int]
    frame_count: int
    timestamp: float
    pose3d: _geometry3d_pb2.ProtobufPose3d
    def __init__(self, frame_count: _Optional[int] = ..., timestamp: _Optional[float] = ..., pose3d: _Optional[_Union[_geometry3d_pb2.ProtobufPose3d, _Mapping]] = ...) -> None: ...

class ProtobufQuestNavDeviceData(_message.Message):
    __slots__ = ("tracking_lost_counter", "currently_tracking", "battery_percent")
    TRACKING_LOST_COUNTER_FIELD_NUMBER: _ClassVar[int]
    CURRENTLY_TRACKING_FIELD_NUMBER: _ClassVar[int]
    BATTERY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    tracking_lost_counter: int
    currently_tracking: bool
    battery_percent: int
    def __init__(self, tracking_lost_counter: _Optional[int] = ..., currently_tracking: bool = ..., battery_percent: _Optional[int] = ...) -> None: ...
