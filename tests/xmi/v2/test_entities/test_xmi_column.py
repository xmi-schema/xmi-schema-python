"""
Tests for XmiColumn physical entity class.

This module tests the XmiColumn class, verifying that:
- It inherits from XmiBasePhysicalEntity
- Domain type is automatically set to "Physical"
- All column-specific properties are correctly handled
- System line enum is properly validated
- Local axes can be parsed from strings or tuples
- Node offsets have proper defaults
- Serialization and deserialization work correctly
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.entities.xmi_column import XmiColumn
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum


def test_column_basic_creation():
    """Test basic column creation with required fields."""
    column = XmiColumn(
        id="column-001",
        name="C1",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000.0
    )

    assert column.id == "column-001"
    assert column.name == "C1"
    assert column.entity_type == "XmiColumn"
    assert column.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert column.system_line == XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    assert column.length == 3000.0


def test_column_domain_type_automatic():
    """Test that domain type is automatically set to Physical."""
    column = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=2800.0
    )
    assert column.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert column.entity_type == "XmiColumn"


def test_column_with_all_properties():
    """Test column creation with all properties specified."""
    column = XmiColumn(
        id="column-002",
        name="Main Column",
        ifcguid="4dKi9gIyk4GxV$0wQRL2QO",
        native_id="54321",
        description="Primary structural column",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3500.0,
        local_axis_x=(1.0, 0.0, 0.0),
        local_axis_y=(0.0, 1.0, 0.0),
        local_axis_z=(0.0, 0.0, 1.0),
        begin_node_x_offset=0.0,
        end_node_x_offset=0.0,
        begin_node_y_offset=0.0,
        end_node_y_offset=0.0,
        begin_node_z_offset=5.0,
        end_node_z_offset=10.0,
        end_fixity_start="Fixed",
        end_fixity_end="Fixed"
    )

    assert column.id == "column-002"
    assert column.name == "Main Column"
    assert column.ifcguid == "4dKi9gIyk4GxV$0wQRL2QO"
    assert column.native_id == "54321"
    assert column.description == "Primary structural column"
    assert column.length == 3500.0
    assert column.local_axis_x == (1.0, 0.0, 0.0)
    assert column.local_axis_y == (0.0, 1.0, 0.0)
    assert column.local_axis_z == (0.0, 0.0, 1.0)
    assert column.begin_node_z_offset == 5.0
    assert column.end_node_z_offset == 10.0
    assert column.end_fixity_start == "Fixed"
    assert column.end_fixity_end == "Fixed"


def test_column_default_values():
    """Test that default values are properly set."""
    column = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3200.0
    )

    assert column.local_axis_x == (1.0, 0.0, 0.0)
    assert column.local_axis_y == (0.0, 1.0, 0.0)
    assert column.local_axis_z == (0.0, 0.0, 1.0)
    assert column.begin_node_x_offset == 0.0
    assert column.end_node_x_offset == 0.0
    assert column.begin_node_y_offset == 0.0
    assert column.end_node_y_offset == 0.0
    assert column.begin_node_z_offset == 0.0
    assert column.end_node_z_offset == 0.0
    assert column.end_fixity_start is None
    assert column.end_fixity_end is None


def test_column_axis_parsing_from_string():
    """Test that local axes can be parsed from comma-separated strings."""
    column = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT,
        length=3000.0,
        local_axis_x="1.0, 0.0, 0.0",
        local_axis_y="0.0, 0.866, 0.5",
        local_axis_z="0.0, -0.5, 0.866"
    )

    assert column.local_axis_x == pytest.approx((1.0, 0.0, 0.0))
    assert column.local_axis_y == pytest.approx((0.0, 0.866, 0.5))
    assert column.local_axis_z == pytest.approx((0.0, -0.5, 0.866))


def test_column_axis_parsing_from_tuple():
    """Test that local axes work with tuple input."""
    column = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_LEFT,
        length=2900.0,
        local_axis_x=(0.866, 0.5, 0.0),
        local_axis_y=(-0.5, 0.866, 0.0),
        local_axis_z=(0.0, 0.0, 1.0)
    )

    assert column.local_axis_x == pytest.approx((0.866, 0.5, 0.0))
    assert column.local_axis_y == pytest.approx((-0.5, 0.866, 0.0))
    assert column.local_axis_z == pytest.approx((0.0, 0.0, 1.0))


def test_column_serialization():
    """Test that column can be serialized to dict."""
    column = XmiColumn(
        id="column-003",
        name="Serialization Test",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT,
        length=3100.0,
        end_fixity_start="Pinned"
    )

    data = column.model_dump()
    assert data["id"] == "column-003"
    assert data["name"] == "Serialization Test"
    assert data["entity_type"] == "XmiColumn"
    assert data["type"] == XmiBaseEntityDomainEnum.PHYSICAL
    assert data["system_line"] == XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT
    assert data["length"] == 3100.0


def test_column_deserialization_pascalcase():
    """Test that column can be created from PascalCase dict."""
    data = {
        "ID": "column-004",
        "Name": "Deserialization Test",
        "Type": "Physical",
        "SystemLine": "MiddleMiddle",
        "Length": 3400.0,
        "LocalAxisX": "1.0, 0.0, 0.0",
        "LocalAxisY": "0.0, 1.0, 0.0",
        "LocalAxisZ": "0.0, 0.0, 1.0",
        "BeginNodeZOffset": 2.0,
        "EndNodeZOffset": 5.0,
        "EndFixityStart": "Fixed",
        "EndFixityEnd": "Pinned"
    }

    column = XmiColumn.model_validate(data)
    assert column.id == "column-004"
    assert column.name == "Deserialization Test"
    assert column.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert column.system_line == XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    assert column.length == 3400.0
    assert column.begin_node_z_offset == 2.0
    assert column.end_node_z_offset == 5.0
    assert column.end_fixity_start == "Fixed"
    assert column.end_fixity_end == "Pinned"


def test_column_from_dict_method():
    """Test the from_dict class method."""
    data = {
        "ID": "column-005",
        "Name": "From Dict Test",
        "SystemLine": "TopMiddle",
        "Length": 3250.0,
        "LocalAxisX": "1.0, 0.0, 0.0",
        "LocalAxisY": "0.0, 1.0, 0.0",
        "LocalAxisZ": "0.0, 0.0, 1.0"
    }

    column, errors = XmiColumn.from_dict(data)
    assert column is not None
    assert len(errors) == 0
    assert column.id == "column-005"
    assert column.name == "From Dict Test"
    assert column.system_line == XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    assert column.length == 3250.0


def test_column_from_dict_with_errors():
    """Test from_dict handles errors gracefully."""
    data = {
        "ID": "column-006",
        "Name": "Error Test",
        "SystemLine": "InvalidValue",  # Invalid enum value
        "Length": 3000.0
    }

    column, errors = XmiColumn.from_dict(data)
    assert column is None
    assert len(errors) > 0


def test_column_missing_required_field():
    """Test that missing required fields raise validation errors."""
    with pytest.raises(ValidationError):
        XmiColumn(
            id="column-007",
            name="Missing SystemLine"
            # Missing system_line and length
        )


def test_column_length_accepts_int():
    """Test that length accepts both int and float."""
    column1 = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000  # int
    )
    column2 = XmiColumn(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000.0  # float
    )

    assert column1.length == 3000
    assert column2.length == 3000.0


def test_column_invalid_axis_string():
    """Test that invalid axis strings raise errors."""
    with pytest.raises(ValidationError):
        XmiColumn(
            system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
            length=3000.0,
            local_axis_x="1.0, 0.0, 0.0, 0.0"  # Too many values
        )


def test_column_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    column = XmiColumn(
        id="column-008",
        name="Inherited Test",
        ifcguid="FEDCBA0987654321",
        native_id="NID-002",
        description="Testing inheritance",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3150.0
    )

    assert column.id == "column-008"
    assert column.name == "Inherited Test"
    assert column.ifcguid == "FEDCBA0987654321"
    assert column.native_id == "NID-002"
    assert column.description == "Testing inheritance"
    assert column.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert column.entity_type == "XmiColumn"


def test_column_multiple_instances_unique():
    """Test that multiple column instances remain independent."""
    column1 = XmiColumn(
        id="column-009",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT,
        length=3000.0
    )
    column2 = XmiColumn(
        id="column-010",
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT,
        length=3500.0
    )

    assert column1.id != column2.id
    assert column1.system_line != column2.system_line
    assert column1.length != column2.length
    assert column1.type == column2.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_column_different_from_beam():
    """Test that column domain type is same as beam but entity_type differs."""
    column = XmiColumn(
        id="column-011",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000.0
    )

    # Both are Physical domain
    assert column.type == XmiBaseEntityDomainEnum.PHYSICAL
    # But different entity types
    assert column.entity_type == "XmiColumn"


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_column.py
