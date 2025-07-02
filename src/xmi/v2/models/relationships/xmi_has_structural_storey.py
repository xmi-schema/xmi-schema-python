from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_storey import XmiStructuralStorey

class XmiHasStructuralStorey(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralStorey):
            raise TypeError("Target must be of type XmiStructuralStorey")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralStorey")
        values.setdefault("entity_type", "XmiRelHasStructuralStorey")
        return values