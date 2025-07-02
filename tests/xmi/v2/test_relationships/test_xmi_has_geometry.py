import pytest
from xmi.v2.models.relationships.xmi_has_geometry import XmiHasGeometry
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_geometry import XmiBaseGeometry

def test_has_geometry_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Beam")
    target = XmiBaseGeometry(id="G1", description="Geometry of Beam")

    rel = XmiHasGeometry(source=source, target=target, IsBegin=True)

    assert rel.source == source
    assert rel.target == target
    assert rel.is_begin is True
    assert rel.is_end is None
    assert rel.name == "hasGeometry"
    assert rel.entity_type == "XmiRelHasGeometry"

def test_invalid_source_type():
    target = XmiBaseGeometry(id="G1", description="Geometry")
    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasGeometry(source="not an entity", target=target)

def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Beam")
    with pytest.raises(TypeError, match="Target must be of type XmiBaseGeometry"):
        XmiHasGeometry(source=source, target="not a geometry")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_geometry.py