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
            raise TypeError("'source' should be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiLine3D):
            raise TypeError("'target' should be of type XmiBaseEntity")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasLine3D")
        values.setdefault("entity_type", "XmiRelHasLine3D")
        return values
    

# Testing run python -m src.xmi.v2.models.relationships.xmi_has_line_3d

if __name__ == "__main__":
    source = XmiBaseEntity(id="E1", name="Column")
    
    start_point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    end_point = XmiPoint3D(x=1.0, y=1.0, z=1.0)
    
    target = XmiLine3D(
        id="E2",
        name="Beam",
        start_point=start_point,
        end_point=end_point
    )

    rel = XmiHasLine3D(source=source, target=target, is_begin=True, is_end=False)

    print("Created XmiHasLine3D relationship:")
    print(rel.model_dump(by_alias=True))