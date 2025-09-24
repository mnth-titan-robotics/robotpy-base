from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtobufTranslation2d(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class ProtobufRotation2d(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class ProtobufPose2d(_message.Message):
    __slots__ = ("translation", "rotation")
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    translation: ProtobufTranslation2d
    rotation: ProtobufRotation2d
    def __init__(self, translation: _Optional[_Union[ProtobufTranslation2d, _Mapping]] = ..., rotation: _Optional[_Union[ProtobufRotation2d, _Mapping]] = ...) -> None: ...

class ProtobufTransform2d(_message.Message):
    __slots__ = ("translation", "rotation")
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    translation: ProtobufTranslation2d
    rotation: ProtobufRotation2d
    def __init__(self, translation: _Optional[_Union[ProtobufTranslation2d, _Mapping]] = ..., rotation: _Optional[_Union[ProtobufRotation2d, _Mapping]] = ...) -> None: ...

class ProtobufTwist2d(_message.Message):
    __slots__ = ("dx", "dy", "dtheta")
    DX_FIELD_NUMBER: _ClassVar[int]
    DY_FIELD_NUMBER: _ClassVar[int]
    DTHETA_FIELD_NUMBER: _ClassVar[int]
    dx: float
    dy: float
    dtheta: float
    def __init__(self, dx: _Optional[float] = ..., dy: _Optional[float] = ..., dtheta: _Optional[float] = ...) -> None: ...

class ProtobufRectangle2d(_message.Message):
    __slots__ = ("center", "xWidth", "yWidth")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    XWIDTH_FIELD_NUMBER: _ClassVar[int]
    YWIDTH_FIELD_NUMBER: _ClassVar[int]
    center: ProtobufPose2d
    xWidth: float
    yWidth: float
    def __init__(self, center: _Optional[_Union[ProtobufPose2d, _Mapping]] = ..., xWidth: _Optional[float] = ..., yWidth: _Optional[float] = ...) -> None: ...

class ProtobufEllipse2d(_message.Message):
    __slots__ = ("center", "xSemiAxis", "ySemiAxis")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    XSEMIAXIS_FIELD_NUMBER: _ClassVar[int]
    YSEMIAXIS_FIELD_NUMBER: _ClassVar[int]
    center: ProtobufPose2d
    xSemiAxis: float
    ySemiAxis: float
    def __init__(self, center: _Optional[_Union[ProtobufPose2d, _Mapping]] = ..., xSemiAxis: _Optional[float] = ..., ySemiAxis: _Optional[float] = ...) -> None: ...
