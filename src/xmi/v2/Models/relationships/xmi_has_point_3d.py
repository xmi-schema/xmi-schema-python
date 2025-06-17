from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..geometries.xmi_point_3d import XmiPoint3D

class XmiHasPoint3D(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("'source' must be an instance of XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiPoint3D):
            raise TypeError("'target' must be an instance of XmiBaseEntity")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasPoint3D")
        values.setdefault("entity_type", "XmiRelHasPoint3D")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_point_3d

if __name__ == "__main__":
    source = XmiBaseEntity(id="N1", name="StartNode", entity_type="Node")
    target = XmiPoint3D(
        id="N2",
        name="Point",
        entity_type="Point3D",
        x=0.0,
        y=1.0,
        z=2.0,
    )

    rel = XmiHasPoint3D(source=source, target=target)

    print("Created XmiHasPoint3D relationship:")
    print(rel.model_dump(by_alias=True))