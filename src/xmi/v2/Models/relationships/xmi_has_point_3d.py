from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..geometries.xmi_point_3d import XmiPoint3D

class XmiHasPoint3D(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiPoint3D):
            raise TypeError("Target must be of type XmiPoint3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasPoint3D")
        values.setdefault("entity_type", "XmiRelHasPoint3D")
        return values