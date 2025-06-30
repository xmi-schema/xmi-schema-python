from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_entity import XmiBaseEntity
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_structural_point_connection import XmiStructuralPointConnection
from .xmi_structural_storey import XmiStructuralStorey
from ..enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from ..geometries.xmi_point_3d import XmiPoint3D

class XmiSegment(XmiBaseEntity):
    geometry: XmiBaseGeometry = Field(..., alias="Geometry")
    position: int = Field(..., alias="Position")
    begin_node: XmiStructuralPointConnection = Field(..., alias="BeginNode")
    end_node: XmiStructuralPointConnection = Field(..., alias="EndNode")
    segment_type: XmiSegmentTypeEnum = Field(..., alias="SegmentType")

    class Config:
        populate_by_name = True

    @field_validator("geometry")
    @classmethod
    def validate_geometry(cls, v):
        if not isinstance(v, XmiBaseGeometry):
            raise TypeError("geometry should be of type XmiBaseGeometry")
        return v

    @field_validator("begin_node", "end_node")
    @classmethod
    def validate_node(cls, v):
        if not isinstance(v, XmiStructuralPointConnection):
            raise TypeError("Nodes should be of type XmiStructuralPointConnection")
        return v

    @field_validator("segment_type")
    @classmethod
    def validate_segment_type(cls, v):
        if not isinstance(v, XmiSegmentTypeEnum):
            raise TypeError("segment_type should be of type XmiSegmentTypeEnum")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("entity_type", "XmiSegment")
        return values

