from pydantic import Field, field_validator, model_validator
from typing import Optional
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..geometries.xmi_line_3d import XmiLine3D
from ..geometries.xmi_point_3d import XmiPoint3D


class XmiHasLine3D(XmiBaseRelationship):
    is_begin: Optional[bool] = Field(default=None, description="Whether this is the beginning of the line relationship")
    is_end: Optional[bool] = Field(default=None, description="Whether this is the end of the line relationship")

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiLine3D):
            raise TypeError("Target must be of type XmiLine3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasLine3D")
        values.setdefault("entity_type", "XmiRelHasLine3D")
        return values
    