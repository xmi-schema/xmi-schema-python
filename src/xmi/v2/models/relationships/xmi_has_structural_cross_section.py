from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_cross_section import XmiStructuralCrossSection

class XmiHasStructuralCrossSection(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralCrossSection):
            raise TypeError("Target must be of type XmiStructuralCrossSection")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralCrossSection")
        values.setdefault("entity_type", "XmiRelHasStructuralCrossSection")
        return values
