from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_segment_type_enum import XmiSegmentTypeEnum

class XmiSegment(XmiBaseEntity):
    position: int = Field(..., alias="Position")
    segment_type: XmiSegmentTypeEnum = Field(..., alias="SegmentType")

    model_config = {
        "populate_by_name": True,
    }

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

