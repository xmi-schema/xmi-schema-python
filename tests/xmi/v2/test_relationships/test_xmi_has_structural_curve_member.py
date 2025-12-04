"""
Tests for XmiHasStructuralCurveMember relationship class.

This module tests the XmiHasStructuralCurveMember relationship, verifying that:
- It properly links physical entities to analytical curve members
- Source validation ensures only physical entities are allowed
- Target validation ensures only structural curve members are allowed
- Default values are correctly set
- The relationship works with both beams and columns
- Serialization and deserialization work correctly
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember
from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
from xmi.v2.models.entities.physical.xmi_column import XmiColumn
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from xmi.v2.models.enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum


def test_relationship_beam_to_curve_member():
    """Test relationship creation from beam to curve member."""
    beam = XmiBeam(
        id="beam-001",
        name="B1",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-001",
        name="CM1",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(source=beam, target=curve_member)

    assert rel.source == beam
    assert rel.target == curve_member
    assert rel.name == "hasStructuralCurveMember"
    assert rel.entity_type == "XmiRelHasStructuralCurveMember"


def test_relationship_column_to_curve_member():
    """Test relationship creation from column to curve member."""
    column = XmiColumn(
        id="column-001",
        name="C1",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-002",
        name="CM2",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.COLUMN,
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(source=column, target=curve_member)

    assert rel.source == column
    assert rel.target == curve_member
    assert rel.name == "hasStructuralCurveMember"
    assert rel.entity_type == "XmiRelHasStructuralCurveMember"


def test_relationship_with_all_properties():
    """Test relationship with all properties specified."""
    beam = XmiBeam(
        id="beam-002",
        name="Main Beam",
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE,
        length=6000.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-003",
        name="Main CM",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(
        id="rel-001",
        source=beam,
        target=curve_member,
        name="customName",
        description="Links physical beam to analytical member",
        uml_type="Association"
    )

    assert rel.id == "rel-001"
    assert rel.source == beam
    assert rel.target == curve_member
    assert rel.name == "customName"
    assert rel.description == "Links physical beam to analytical member"
    assert rel.uml_type == "Association"
    assert rel.entity_type == "XmiRelHasStructuralCurveMember"


def test_relationship_default_values():
    """Test that default values are properly set."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    curve_member = XmiStructuralCurveMember(
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(source=beam, target=curve_member)

    assert rel.name == "hasStructuralCurveMember"
    assert rel.entity_type == "XmiRelHasStructuralCurveMember"
    assert rel.id is not None  # Auto-generated UUID
    assert len(rel.id) > 0


def test_invalid_source_type_not_physical():
    """Test that non-physical entity sources are rejected."""
    # Use base entity which is not physical
    source = XmiBaseEntity(id="E1", name="Not Physical")

    curve_member = XmiStructuralCurveMember(
        id="cm-004",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBasePhysicalEntity"):
        XmiHasStructuralCurveMember(source=source, target=curve_member)


def test_invalid_source_type_string():
    """Test that string sources are rejected."""
    curve_member = XmiStructuralCurveMember(
        id="cm-005",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    with pytest.raises(TypeError, match="Source must be of type XmiBasePhysicalEntity"):
        XmiHasStructuralCurveMember(source="not a physical entity", target=curve_member)


def test_invalid_target_type_not_curve_member():
    """Test that non-curve-member targets are rejected."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    # Use base entity instead of curve member
    target = XmiBaseEntity(id="E2", name="Not Curve Member")

    with pytest.raises(TypeError, match="Target must be of type XmiStructuralCurveMember"):
        XmiHasStructuralCurveMember(source=beam, target=target)


def test_invalid_target_type_string():
    """Test that string targets are rejected."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    with pytest.raises(TypeError, match="Target must be of type XmiStructuralCurveMember"):
        XmiHasStructuralCurveMember(source=beam, target="not a curve member")


def test_relationship_serialization():
    """Test that relationship can be serialized to dict."""
    beam = XmiBeam(
        id="beam-003",
        name="Serialization Test Beam",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT,
        length=7000.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-006",
        name="Serialization Test CM",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_RIGHT
    )

    rel = XmiHasStructuralCurveMember(
        id="rel-002",
        source=beam,
        target=curve_member
    )

    data = rel.model_dump()
    assert data["id"] == "rel-002"
    assert data["name"] == "hasStructuralCurveMember"
    assert data["entity_type"] == "XmiRelHasStructuralCurveMember"
    # Check that source and target are serialized as dicts
    assert isinstance(data["source"], dict)
    assert isinstance(data["target"], dict)
    assert data["source"]["id"] == "beam-003"
    assert data["target"]["id"] == "cm-006"


def test_relationship_with_custom_name():
    """Test that custom name can be provided."""
    beam = XmiBeam(
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    curve_member = XmiStructuralCurveMember(
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(
        source=beam,
        target=curve_member,
        name="CustomRelationshipName"
    )

    assert rel.name == "CustomRelationshipName"
    assert rel.entity_type == "XmiRelHasStructuralCurveMember"


def test_relationship_with_description():
    """Test relationship with description."""
    column = XmiColumn(
        id="column-002",
        name="C2",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3500.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-007",
        name="CM7",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.COLUMN,
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    )

    rel = XmiHasStructuralCurveMember(
        source=column,
        target=curve_member,
        description="Primary column to analytical member mapping"
    )

    assert rel.description == "Primary column to analytical member mapping"


def test_multiple_relationships_same_entities():
    """Test that multiple relationships can reference same entities."""
    beam = XmiBeam(
        id="beam-004",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-008",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    rel1 = XmiHasStructuralCurveMember(source=beam, target=curve_member)
    rel2 = XmiHasStructuralCurveMember(source=beam, target=curve_member)

    # Relationships should be different instances with different IDs
    assert rel1 is not rel2
    assert rel1.id != rel2.id
    # But reference the same entities
    assert rel1.source == rel2.source == beam
    assert rel1.target == rel2.target == curve_member


def test_relationship_different_system_lines():
    """Test relationship works with entities having different system lines."""
    beam = XmiBeam(
        id="beam-005",
        name="Beam TopLeft",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT,
        length=4500.0
    )

    curve_member = XmiStructuralCurveMember(
        id="cm-009",
        name="CM BottomRight",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT
    )

    # Should still create relationship even with different system lines
    # (validation of system line compatibility is not enforced at relationship level)
    rel = XmiHasStructuralCurveMember(source=beam, target=curve_member)

    assert rel.source.system_line == XmiStructuralCurveMemberSystemLineEnum.TOP_LEFT
    assert rel.target.system_line == XmiStructuralCurveMemberSystemLineEnum.BOTTOM_RIGHT


def test_relationship_beam_and_column_types():
    """Test relationships with both beam and column types."""
    beam = XmiBeam(
        id="beam-006",
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE,
        length=5000.0
    )

    column = XmiColumn(
        id="column-003",
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE,
        length=3000.0
    )

    cm_beam = XmiStructuralCurveMember(
        id="cm-010",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.BEAM,
        system_line=XmiStructuralCurveMemberSystemLineEnum.TOP_MIDDLE
    )

    cm_column = XmiStructuralCurveMember(
        id="cm-011",
        curve_member_type=XmiStructuralCurveMemberTypeEnum.COLUMN,
        system_line=XmiStructuralCurveMemberSystemLineEnum.MIDDLE_MIDDLE
    )

    rel_beam = XmiHasStructuralCurveMember(source=beam, target=cm_beam)
    rel_column = XmiHasStructuralCurveMember(source=column, target=cm_column)

    assert rel_beam.source.entity_type == "XmiBeam"
    assert rel_column.source.entity_type == "XmiColumn"
    assert rel_beam.target.curve_member_type == XmiStructuralCurveMemberTypeEnum.BEAM
    assert rel_column.target.curve_member_type == XmiStructuralCurveMemberTypeEnum.COLUMN


# Run with: pytest tests/xmi/v2/test_relationships/test_xmi_has_structural_curve_member.py
