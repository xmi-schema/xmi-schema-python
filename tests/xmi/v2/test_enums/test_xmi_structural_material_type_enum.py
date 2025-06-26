from src.xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

def test_enum_values():
    assert XmiStructuralMaterialTypeEnum.CONCRETE.value == "Concrete"
    assert XmiStructuralMaterialTypeEnum.STEEL.value == "Steel"
    assert XmiStructuralMaterialTypeEnum.TIMBER.value == "Timber"
    assert XmiStructuralMaterialTypeEnum.ALUMINIUM.value == "Aluminium"
    assert XmiStructuralMaterialTypeEnum.COMPOSITE.value == "Composite"
    assert XmiStructuralMaterialTypeEnum.MASONRY.value == "Masonry"
    assert XmiStructuralMaterialTypeEnum.OTHERS.value == "Others"
    assert XmiStructuralMaterialTypeEnum.REBAR.value == "Rebar"
    assert XmiStructuralMaterialTypeEnum.TENDON.value == "Tendon"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_material_type_enum.py