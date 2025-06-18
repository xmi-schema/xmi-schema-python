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
    from ..enums.xmi_segment_type_enum import XmiSegmentTypeEnum
    from ..geometries.xmi_point_3d import XmiPoint3D
    from ..bases.xmi_base_geometry import XmiBaseGeometry
    from ..entities.xmi_structural_point_connection import XmiStructuralPointConnection
    from ..entities.xmi_structural_storey import XmiStructuralStorey

    geometry = XmiBaseGeometry(id="g1", name="Geometry1")
    storey = XmiStructuralStorey(id="s1", name="Storey1", storey_elevation=0.0)

    point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    begin_node = XmiStructuralPointConnection(id="n1", name="Begin", point=point, storey=storey)
    end_node = XmiStructuralPointConnection(id="n2", name="End", point=point, storey=storey)

    target = XmiSegment(
        id="E2",
        name="Segment1",
        geometry=geometry,
        position=1,
        begin_node=begin_node,
        end_node=end_node,
        segment_type=XmiSegmentTypeEnum.LINE
    )

    source = XmiBaseEntity(id="E1", name="MainElement", entity_type="StructuralElement")

    rel = XmiHasSegment(source=source, target=target)

    print("Created XmiHasSegment relationship:")
    print(rel.model_dump(by_alias=True))