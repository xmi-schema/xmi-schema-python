import pytest
from xmi.v2.models.relationships.xmi_has_point_3d import XmiHasPoint3D
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D


def test_has_point_3d_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Node")
    target = XmiPoint3D(x=1.0, y=2.0, z=3.0)

    rel = XmiHasPoint3D(source=source, target=target)

    assert rel.source == source
    assert rel.target == target
    assert rel.name == "hasPoint3D"
    assert rel.entity_type == "XmiRelHasPoint3D"


def test_invalid_source_type():
    target = XmiPoint3D(x=1.0, y=2.0, z=3.0)
    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasPoint3D(source="not a base entity", target=target)


def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Node")
    with pytest.raises(TypeError, match="Target must be of type XmiPoint3D"):
        XmiHasPoint3D(source=source, target="not a point")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_point_3d.py