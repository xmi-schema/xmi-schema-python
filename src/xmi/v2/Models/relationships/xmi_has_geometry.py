from pydantic import Field, field_validator, model_validator
from typing import Optional
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..bases.xmi_base_geometry import XmiBaseGeometry

class XmiHasGeometry(XmiBaseRelationship):
    is_begin: Optional[bool] = Field(default=None, alias="IsBegin", description="Whether this is the beginning of the geometry relationship")
    is_end: Optional[bool] = Field(default=None, alias="IsEnd", description="Whether this is the end of the geometry relationship")

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiBaseGeometry):
            raise TypeError("Target must be of type XmiBaseGeometry")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasGeometry")
        values.setdefault("entity_type", "XmiRelHasGeometry")
        return values
