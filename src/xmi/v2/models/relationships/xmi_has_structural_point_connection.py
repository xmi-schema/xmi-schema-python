from pydantic import Field, field_validator, model_validator
from typing import Optional
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_structural_point_connection import XmiStructuralPointConnection

class XmiHasStructuralPointConnection(XmiBaseRelationship):
    is_begin: Optional[bool] = Field(None, alias="IsBegin")
    is_end: Optional[bool] = Field(None, alias="IsEnd")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @field_validator("source")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source should be of type XmiBaseEntity")
        return v

    @field_validator("target")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralPointConnection):
            raise TypeError("Target should be of type XmiStructuralPointConnection")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralPointConnection")
        values.setdefault("entity_type", "XmiRelHasStructuralPointConnection")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_structural_point_connection
if __name__ == "__main__":
    from src.xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey
    from src.xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

    storey = XmiStructuralStorey(
        id="storey001",
        name="Level 1",
        storey_elevation=0,
        description="Ground level"
    )

    point_conn = XmiStructuralPointConnection(
        id="node001",
        name="Connection A",
        point=XmiPoint3D(x=1.0, y=2.0, z=3.0),
        storey=storey
    )

    source_entity = storey

    rel = XmiHasStructuralPointConnection(
        source=source_entity,
        target=point_conn,
        is_begin=True,
        is_end=False
    )

    print("Created XmiHasStructuralPointConnection relationship:")
    print(rel.model_dump(by_alias=True))