import pytest
from xmi.v2.models.relationships.xmi_has_segment import XmiHasSegment
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_segment import XmiSegment
from xmi.v2.models.bases.xmi_base_geometry import XmiBaseGeometry
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D


def test_has_segment_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Beam")

    geometry = XmiBaseGeometry()
    point = XmiPoint3D(x=0.0, y=0.0, z=0.0)

    start_connection = XmiStructuralPointConnection(id="P1", node_id="N1", point=point)
    end_connection = XmiStructuralPointConnection(id="P2", node_id="N2", point=point)

    segment = XmiSegment(
        id="S1",
        description="Test segment",
        segment_type=XmiSegmentTypeEnum.LINE,
        geometry=geometry,
        start_connection=start_connection,
        end_connection=end_connection,
        position=0
    )

    rel = XmiHasSegment(source=source, target=segment)

    assert rel.source == source
    assert rel.target == segment
    assert rel.name == "hasSegment"
    assert rel.entity_type == "XmiRelHasSegment"


def test_invalid_source_type():
    geometry = XmiBaseGeometry()
    point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    start_connection = XmiStructuralPointConnection(id="P1", node_id="N1", point=point)
    end_connection = XmiStructuralPointConnection(id="P2", node_id="N2", point=point)

    segment = XmiSegment(
        id="S1",
        segment_type=XmiSegmentTypeEnum.LINE,
        geometry=geometry,
        start_connection=start_connection,
        end_connection=end_connection,
        position=0
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasSegment(source="not a base entity", target=segment)


def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Beam")

    with pytest.raises(TypeError, match="Target must be of type Xmi"):
        XmiHasSegment(source=source, target="not a segment")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_segment.py