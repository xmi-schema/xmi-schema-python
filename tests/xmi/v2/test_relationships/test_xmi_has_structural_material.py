import pytest
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.entities.xmi_structural_material import XmiStructuralMaterial
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

def test_has_structural_material_valid_instantiation():
    source = XmiBaseEntity(id="E1", name="Column")
    material = XmiStructuralMaterial(
        id="M1",
        material_type=XmiStructuralMaterialTypeEnum.CONCRETE,
        grade=30.0,
        unit_weight=25.0,
        e_modulus=(30000.0, 30000.0, 30000.0),
        g_modulus=(12000.0, 12000.0, 12000.0),
        poisson_ratio=(0.2, 0.2, 0.2),
        thermal_coefficient=1e-5,
    )
    rel = XmiHasStructuralMaterial(source=source, target=material)
    assert rel.source == source
    assert rel.target == material
    assert rel.name == "hasStructuralMaterial"
    assert rel.entity_type == "XmiRelHasStructuralMaterial"

def test_invalid_source_type():
    material = XmiStructuralMaterial(
        id="M1",
        material_type=XmiStructuralMaterialTypeEnum.STEEL,
        grade=50.0,
        unit_weight=78.5,
        e_modulus=(200000.0, 200000.0, 200000.0),
        g_modulus=(80000.0, 80000.0, 80000.0),
        poisson_ratio=(0.3, 0.3, 0.3),
        thermal_coefficient=1.2e-5,
    )
    with pytest.raises(TypeError, match="Source must be of type XmiBaseEntity"):
        XmiHasStructuralMaterial(source="not a base entity", target=material)

def test_invalid_target_type():
    source = XmiBaseEntity(id="E1", name="Column")
    with pytest.raises(TypeError, match="Target must be of type XmiStructuralMaterial"):
        XmiHasStructuralMaterial(source=source, target="not a base entity")


# .venv/bin/python -m pytest tests/xmi/v2/test_relationships/test_xmi_has_structural_material.py