import pytest
from xmi.v2.models.enums.xmi_structural_material_type_enum import XmiStructuralMaterialTypeEnum

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


def test_from_name_get_enum_valid():
    """Test from_name_get_enum with valid enum names"""
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("CONCRETE") == XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("concrete") == XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("STEEL") == XmiStructuralMaterialTypeEnum.STEEL
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("steel") == XmiStructuralMaterialTypeEnum.STEEL


def test_from_name_get_enum_invalid():
    """Test from_name_get_enum with invalid enum name returns None"""
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("INVALID_MATERIAL") is None
    assert XmiStructuralMaterialTypeEnum.from_name_get_enum("NonExistent") is None


def test_from_attribute_get_enum_with_string():
    """Test from_attribute_get_enum with string attribute values"""
    assert XmiStructuralMaterialTypeEnum.from_attribute_get_enum("Concrete") == XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum.from_attribute_get_enum("Steel") == XmiStructuralMaterialTypeEnum.STEEL
    assert XmiStructuralMaterialTypeEnum.from_attribute_get_enum("Timber") == XmiStructuralMaterialTypeEnum.TIMBER


def test_from_attribute_get_enum_with_enum():
    """Test from_attribute_get_enum with enum instance returns same instance"""
    concrete_enum = XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum.from_attribute_get_enum(concrete_enum) == XmiStructuralMaterialTypeEnum.CONCRETE


def test_from_attribute_get_enum_invalid():
    """Test from_attribute_get_enum with invalid value raises ValueError"""
    with pytest.raises(ValueError, match="Invalid XmiStructuralMaterialTypeEnum value"):
        XmiStructuralMaterialTypeEnum.from_attribute_get_enum("InvalidMaterial")


def test_case_insensitive_lookup():
    """Test that enum lookup is case-insensitive"""
    # Using the value directly should work with any case
    assert XmiStructuralMaterialTypeEnum("concrete") == XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum("CONCRETE") == XmiStructuralMaterialTypeEnum.CONCRETE
    assert XmiStructuralMaterialTypeEnum("Concrete") == XmiStructuralMaterialTypeEnum.CONCRETE


def test_missing_with_non_string_returns_none():
    """Test _missing_ method returns None for non-string values"""
    # This tests the internal _missing_ method indirectly
    result = XmiStructuralMaterialTypeEnum._missing_(123)
    assert result is None


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_structural_material_type_enum.py