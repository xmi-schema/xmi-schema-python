import pytest
from xmi.v2.models.relationships.xmi_has_storey import XmiHasStorey
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_storey import XmiStorey

def test_has_storey_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Building")
    target = XmiStorey(
        id="S1",
        name="Storey 1",
        native_id="S1",
        storey_elevation=0.0,
        storey_mass=1000.0,
    )

    rel = XmiHasStorey(source=source, target=target)

    assert rel.source == source
    assert rel.target == target
    assert rel.name == "hasStructuralStorey"
    assert rel.entity_type == "XmiRelHasStructuralStorey"

def test_invalid_source_type():
    target = XmiStorey(
        id="S1",
        name="Storey 1",
        native_id="S1",
        storey_elevation=0.0,
        storey_mass=1000.0,
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasStorey(source="invalid source", target=target)

def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Building")

    with pytest.raises(TypeError, match="Target must be of type XmiStorey"):
        XmiHasStorey(source=source, target="invalid target")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_storey.py