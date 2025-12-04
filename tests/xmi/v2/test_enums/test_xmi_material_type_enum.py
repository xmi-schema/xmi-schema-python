import pytest
from xmi.v2.models.enums.xmi_material_type_enum import XmiMaterialTypeEnum

def test_enum_values():
    assert XmiMaterialTypeEnum.CONCRETE.value == "Concrete"
    assert XmiMaterialTypeEnum.STEEL.value == "Steel"
    assert XmiMaterialTypeEnum.TIMBER.value == "Timber"
    assert XmiMaterialTypeEnum.ALUMINIUM.value == "Aluminium"
    assert XmiMaterialTypeEnum.COMPOSITE.value == "Composite"
    assert XmiMaterialTypeEnum.MASONRY.value == "Masonry"
    assert XmiMaterialTypeEnum.OTHERS.value == "Others"
    assert XmiMaterialTypeEnum.REBAR.value == "Rebar"
    assert XmiMaterialTypeEnum.TENDON.value == "Tendon"


def test_from_name_get_enum_valid():
    """Test from_name_get_enum with valid enum names"""
    assert XmiMaterialTypeEnum.from_name_get_enum("CONCRETE") == XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum.from_name_get_enum("concrete") == XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum.from_name_get_enum("STEEL") == XmiMaterialTypeEnum.STEEL
    assert XmiMaterialTypeEnum.from_name_get_enum("steel") == XmiMaterialTypeEnum.STEEL


def test_from_name_get_enum_invalid():
    """Test from_name_get_enum with invalid enum name returns None"""
    assert XmiMaterialTypeEnum.from_name_get_enum("INVALID_MATERIAL") is None
    assert XmiMaterialTypeEnum.from_name_get_enum("NonExistent") is None


def test_from_attribute_get_enum_with_string():
    """Test from_attribute_get_enum with string attribute values"""
    assert XmiMaterialTypeEnum.from_attribute_get_enum("Concrete") == XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum.from_attribute_get_enum("Steel") == XmiMaterialTypeEnum.STEEL
    assert XmiMaterialTypeEnum.from_attribute_get_enum("Timber") == XmiMaterialTypeEnum.TIMBER


def test_from_attribute_get_enum_with_enum():
    """Test from_attribute_get_enum with enum instance returns same instance"""
    concrete_enum = XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum.from_attribute_get_enum(concrete_enum) == XmiMaterialTypeEnum.CONCRETE


def test_from_attribute_get_enum_invalid():
    """Test from_attribute_get_enum with invalid value raises ValueError"""
    with pytest.raises(ValueError, match="Invalid XmiMaterialTypeEnum value"):
        XmiMaterialTypeEnum.from_attribute_get_enum("InvalidMaterial")


def test_case_insensitive_lookup():
    """Test that enum lookup is case-insensitive"""
    # Using the value directly should work with any case
    assert XmiMaterialTypeEnum("concrete") == XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum("CONCRETE") == XmiMaterialTypeEnum.CONCRETE
    assert XmiMaterialTypeEnum("Concrete") == XmiMaterialTypeEnum.CONCRETE


def test_missing_with_non_string_returns_none():
    """Test _missing_ method returns None for non-string values"""
    # This tests the internal _missing_ method indirectly
    result = XmiMaterialTypeEnum._missing_(123)
    assert result is None


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_material_type_enum.py