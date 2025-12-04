"""
Tests for XmiBeam physical entity class.

This module tests the XmiBeam class, verifying that:
- It inherits from XmiBasePhysicalEntity
- Domain type is automatically set to "Physical"
- All beam-specific properties are correctly handled
- System line enum is properly validated
- Local axes can be parsed from strings or tuples
- Node offsets have proper defaults
- Serialization and deserialization work correctly
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum


def test_beam_basic_creation():
    """Test basic beam creation with required fields."""
    beam = XmiBeam(
        id="beam-001",
        name="B1",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    assert beam.id == "beam-001"
    assert beam.name == "B1"
    assert beam.entity_type == "XmiBeam"
    assert beam.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert beam.system_line == XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    assert beam.length == 5000.0


def test_beam_domain_type_automatic():
    """Test that domain type is automatically set to Physical."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3500.0
    )
    assert beam.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert beam.entity_type == "XmiBeam"


def test_beam_with_all_properties():
    """Test beam creation with all properties specified."""
    beam = XmiBeam(
        id="beam-002",
        name="Main Beam",
        ifcguid="3cJh8fHxj3FwU$9vPQK1PN",
        native_id="12345",
        description="Primary structural beam",
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE,
        length=6000.0,
        local_axis_x=(1.0, 0.0, 0.0),
        local_axis_y=(0.0, 1.0, 0.0),
        local_axis_z=(0.0, 0.0, 1.0),
        begin_node_x_offset=10.0,
        end_node_x_offset=15.0,
        begin_node_y_offset=5.0,
        end_node_y_offset=5.0,
        begin_node_z_offset=0.0,
        end_node_z_offset=0.0
    )

    assert beam.id == "beam-002"
    assert beam.name == "Main Beam"
    assert beam.ifcguid == "3cJh8fHxj3FwU$9vPQK1PN"
    assert beam.native_id == "12345"
    assert beam.description == "Primary structural beam"
    assert beam.length == 6000.0
    assert beam.local_axis_x == (1.0, 0.0, 0.0)
    assert beam.local_axis_y == (0.0, 1.0, 0.0)
    assert beam.local_axis_z == (0.0, 0.0, 1.0)
    assert beam.begin_node_x_offset == 10.0
    assert beam.end_node_x_offset == 15.0


def test_beam_default_values():
    """Test that default values are properly set."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=4000.0
    )

    assert beam.local_axis_x == (1.0, 0.0, 0.0)
    assert beam.local_axis_y == (0.0, 1.0, 0.0)
    assert beam.local_axis_z == (0.0, 0.0, 1.0)
    assert beam.begin_node_x_offset == 0.0
    assert beam.end_node_x_offset == 0.0
    assert beam.begin_node_y_offset == 0.0
    assert beam.end_node_y_offset == 0.0
    assert beam.begin_node_z_offset == 0.0
    assert beam.end_node_z_offset == 0.0


def test_beam_axis_parsing_from_string():
    """Test that local axes can be parsed from comma-separated strings."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT,
        length=5000.0,
        local_axis_x="0.707, 0.707, 0.0",
        local_axis_y="-0.707, 0.707, 0.0",
        local_axis_z="0.0, 0.0, 1.0"
    )

    assert beam.local_axis_x == pytest.approx((0.707, 0.707, 0.0))
    assert beam.local_axis_y == pytest.approx((-0.707, 0.707, 0.0))
    assert beam.local_axis_z == pytest.approx((0.0, 0.0, 1.0))


def test_beam_axis_parsing_from_tuple():
    """Test that local axes work with tuple input."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_LEFT,
        length=4500.0,
        local_axis_x=(0.5, 0.866, 0.0),
        local_axis_y=(-0.866, 0.5, 0.0),
        local_axis_z=(0.0, 0.0, 1.0)
    )

    assert beam.local_axis_x == pytest.approx((0.5, 0.866, 0.0))
    assert beam.local_axis_y == pytest.approx((-0.866, 0.5, 0.0))
    assert beam.local_axis_z == pytest.approx((0.0, 0.0, 1.0))


def test_beam_serialization():
    """Test that beam can be serialized to dict."""
    beam = XmiBeam(
        id="beam-003",
        name="Serialization Test",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT,
        length=7000.0
    )

    data = beam.model_dump()
    assert data["id"] == "beam-003"
    assert data["name"] == "Serialization Test"
    assert data["entity_type"] == "XmiBeam"
    assert data["type"] == XmiBaseEntityDomainEnum.PHYSICAL
    assert data["system_line"] == XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT
    assert data["length"] == 7000.0


def test_beam_deserialization_pascalcase():
    """Test that beam can be created from PascalCase dict."""
    data = {
        "ID": "beam-004",
        "Name": "Deserialization Test",
        "Type": "Physical",
        "SystemLine": "TopMiddle",
        "Length": 5500.0,
        "LocalAxisX": "1.0, 0.0, 0.0",
        "LocalAxisY": "0.0, 1.0, 0.0",
        "LocalAxisZ": "0.0, 0.0, 1.0",
        "BeginNodeXOffset": 5.0,
        "EndNodeXOffset": 10.0
    }

    beam = XmiBeam.model_validate(data)
    assert beam.id == "beam-004"
    assert beam.name == "Deserialization Test"
    assert beam.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert beam.system_line == XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    assert beam.length == 5500.0
    assert beam.begin_node_x_offset == 5.0
    assert beam.end_node_x_offset == 10.0


def test_beam_from_dict_method():
    """Test the from_dict class method."""
    data = {
        "ID": "beam-005",
        "Name": "From Dict Test",
        "SystemLine": "MiddleMiddle",
        "Length": 4800.0,
        "LocalAxisX": "1.0, 0.0, 0.0",
        "LocalAxisY": "0.0, 1.0, 0.0",
        "LocalAxisZ": "0.0, 0.0, 1.0"
    }

    beam, errors = XmiBeam.from_dict(data)
    assert beam is not None
    assert len(errors) == 0
    assert beam.id == "beam-005"
    assert beam.name == "From Dict Test"
    assert beam.system_line == XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    assert beam.length == 4800.0


def test_beam_from_dict_with_errors():
    """Test from_dict handles errors gracefully."""
    data = {
        "ID": "beam-006",
        "Name": "Error Test",
        "SystemLine": "InvalidValue",  # Invalid enum value
        "Length": 5000.0
    }

    beam, errors = XmiBeam.from_dict(data)
    assert beam is None
    assert len(errors) > 0


def test_beam_missing_required_field():
    """Test that missing required fields raise validation errors."""
    with pytest.raises(ValidationError):
        XmiBeam(
            id="beam-007",
            name="Missing SystemLine"
            # Missing system_line and length
        )


def test_beam_length_accepts_int():
    """Test that length accepts both int and float."""
    beam1 = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE,
        length=5000  # int
    )
    beam2 = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE,
        length=5000.0  # float
    )

    assert beam1.length == 5000
    assert beam2.length == 5000.0


def test_beam_invalid_axis_string():
    """Test that invalid axis strings raise errors."""
    with pytest.raises(ValidationError):
        XmiBeam(
            system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
            length=5000.0,
            local_axis_x="1.0, 0.0"  # Only 2 values instead of 3
        )


def test_beam_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    beam = XmiBeam(
        id="beam-008",
        name="Inherited Test",
        ifcguid="1234567890ABCDEF",
        native_id="NID-001",
        description="Testing inheritance",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=6500.0
    )

    assert beam.id == "beam-008"
    assert beam.name == "Inherited Test"
    assert beam.ifcguid == "1234567890ABCDEF"
    assert beam.native_id == "NID-001"
    assert beam.description == "Testing inheritance"
    assert beam.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert beam.entity_type == "XmiBeam"


def test_beam_multiple_instances_unique():
    """Test that multiple beam instances remain independent."""
    beam1 = XmiBeam(
        id="beam-009",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT,
        length=5000.0
    )
    beam2 = XmiBeam(
        id="beam-010",
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT,
        length=6000.0
    )

    assert beam1.id != beam2.id
    assert beam1.system_line != beam2.system_line
    assert beam1.length != beam2.length
    assert beam1.type == beam2.type == XmiBaseEntityDomainEnum.PHYSICAL


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_beam.py
