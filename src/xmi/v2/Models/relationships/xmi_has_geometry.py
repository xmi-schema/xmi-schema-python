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
            raise TypeError("'source' should be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiBaseGeometry):
            raise TypeError("'target' should be of type XmiBaseGeometry")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasGeometry")
        values.setdefault("entity_type", "XmiRelHasGeometry")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_geometry

if __name__ == "__main__":
    source = XmiBaseEntity(id="E1", name="Beam")
    target = XmiBaseGeometry(id="G1", description="Geometry of Beam")

    rel = XmiHasGeometry(
        source=source,
        target=target
    )

    print("Created XmiHasGeometry relationship:")
    print(rel.model_dump(by_alias=True))