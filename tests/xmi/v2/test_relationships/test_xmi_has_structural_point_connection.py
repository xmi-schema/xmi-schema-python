import pytest
from xmi.v2.models.relationships.xmi_has_structural_point_connection import XmiHasStructuralPointConnection
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

def test_has_structural_point_connection_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Column")
    point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    target = XmiStructuralPointConnection(id="P1", node_id="N1", point=point)

    rel = XmiHasStructuralPointConnection(
        source=source,
        target=target,
        is_begin=True,
        is_end=False,
    )

    assert rel.source == source
    assert rel.target == target
    assert rel.is_begin is True
    assert rel.is_end is False
    assert rel.name == "hasStructuralPointConnection"
    assert rel.entity_type == "XmiRelHasStructuralPointConnection"

def test_invalid_source_type():
    point = XmiPoint3D(x=0.0, y=0.0, z=0.0)
    target = XmiStructuralPointConnection(id="P1", node_id="N1", point=point)

    with pytest.raises(TypeError, match="Source should be of type XmiBaseEntity"):
        XmiHasStructuralPointConnection(source="not a base entity", target=target)

def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Column")

    with pytest.raises(TypeError, match="Target should be of type XmiStructuralPointConnection"):
        XmiHasStructuralPointConnection(source=source, target="not a point connection")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_structural_point_connection.py