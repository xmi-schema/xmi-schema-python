import pytest
from xmi.v2.models.relationships.xmi_has_line_3d import XmiHasLine3D
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.geometries.xmi_line_3d import XmiLine3D
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D


def test_has_line_3d_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Column")
    target = XmiLine3D(
        id="L1",
        description="Line geometry",
        start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
        end_point=XmiPoint3D(x=1.0, y=1.0, z=1.0)
    )

    rel = XmiHasLine3D(source=source, target=target, is_begin=True)

    assert rel.source == source
    assert rel.target == target
    assert rel.is_begin is True
    assert rel.is_end is None
    assert rel.name == "hasLine3D"
    assert rel.entity_type == "XmiRelHasLine3D"


def test_invalid_source_type():
    target = XmiLine3D(
        id="L1",
        description="Line geometry",
        start_point=XmiPoint3D(x=0.0, y=0.0, z=0.0),
        end_point=XmiPoint3D(x=1.0, y=1.0, z=1.0)
    )
    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasLine3D(source="not an entity", target=target)


def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Column")
    with pytest.raises(TypeError, match="Target must be of type XmiLine3D"):
        XmiHasLine3D(source=source, target="not a line")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_line_3d.py