from pydantic import field_validator, model_validator
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.xmi_segment import XmiSegment


class XmiHasSegment(XmiBaseRelationship):
    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("'source' must be an instance of XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiSegment):
            raise TypeError("'target' must be an instance of XmiBaseEntity")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasSegment")
        values.setdefault("entity_type", "XmiRelHasSegment")
        return values


# Testing run python -m src.xmi.v2.models.relationships.xmi_has_segment
if __name__ == "__main__":
    source = XmiBaseEntity(id="E1", name="MainElement", entity_type="StructuralElement")
    target = XmiSegment(id="E2", name="Segment1", entity_type="Segment")

    rel = XmiHasSegment(source=source, target=target)

    print("Created XmiHasSegment relationship:")
    print(rel.model_dump(by_alias=True))