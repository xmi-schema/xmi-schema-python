"""
Tests for XmiWall physical entity class.

This module tests the XmiWall class, verifying that:
- It inherits from XmiBasePhysicalEntity
- Domain type is automatically set to "Physical"
- All inherited properties work correctly
- Serialization and deserialization work correctly
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.entities.physical.xmi_wall import XmiWall
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


def test_wall_basic_creation():
    """Test basic wall creation."""
    wall = XmiWall(
        id="wall-001",
        name="Exterior Wall A"
    )

    assert wall.id == "wall-001"
    assert wall.name == "Exterior Wall A"
    assert wall.entity_type == "XmiWall"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_domain_type_automatic():
    """Test that domain type is automatically set to Physical."""
    wall = XmiWall()
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert wall.entity_type == "XmiWall"


def test_wall_with_all_properties():
    """Test wall creation with all inherited properties specified."""
    wall = XmiWall(
        id="wall-002",
        name="Load Bearing Wall",
        ifcguid="6fMk1iKzm6IzX$2yUSN4RQ",
        native_id="11111",
        description="Concrete load-bearing wall"
    )

    assert wall.id == "wall-002"
    assert wall.name == "Load Bearing Wall"
    assert wall.ifcguid == "6fMk1iKzm6IzX$2yUSN4RQ"
    assert wall.native_id == "11111"
    assert wall.description == "Concrete load-bearing wall"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert wall.entity_type == "XmiWall"


def test_wall_default_id_generation():
    """Test that ID is auto-generated when not provided."""
    wall = XmiWall()
    assert wall.id is not None
    assert len(wall.id) > 0
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_name_defaults_to_id():
    """Test that name defaults to ID when not provided."""
    wall = XmiWall(id="wall-id-789")
    assert wall.name == "wall-id-789"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_optional_fields():
    """Test that optional fields can be None."""
    wall = XmiWall(id="wall-003")
    assert wall.ifcguid is None
    assert wall.native_id is None
    assert wall.description is None
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_serialization():
    """Test that wall can be serialized to dict."""
    wall = XmiWall(
        id="wall-004",
        name="Serialization Test",
        description="Test serialization"
    )

    data = wall.model_dump()
    assert data["id"] == "wall-004"
    assert data["name"] == "Serialization Test"
    assert data["entity_type"] == "XmiWall"
    assert data["type"] == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_deserialization_pascalcase():
    """Test that wall can be created from PascalCase dict."""
    data = {
        "ID": "wall-005",
        "Name": "Deserialization Test",
        "Type": "Physical",
        "Description": "Test deserialization"
    }

    wall = XmiWall.model_validate(data)
    assert wall.id == "wall-005"
    assert wall.name == "Deserialization Test"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert wall.description == "Test deserialization"


def test_wall_deserialization_snake_case():
    """Test that wall can be created from snake_case dict."""
    data = {
        "id": "wall-006",
        "name": "Snake Case Test",
        "type": "Physical",
        "description": "Test snake_case"
    }

    wall = XmiWall.model_validate(data)
    assert wall.id == "wall-006"
    assert wall.name == "Snake Case Test"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_from_dict_method():
    """Test the from_dict class method."""
    data = {
        "ID": "wall-007",
        "Name": "From Dict Test",
        "NativeId": "22222",
        "Description": "Testing from_dict method"
    }

    wall, errors = XmiWall.from_dict(data)
    assert wall is not None
    assert len(errors) == 0
    assert wall.id == "wall-007"
    assert wall.name == "From Dict Test"
    assert wall.native_id == "22222"
    assert wall.description == "Testing from_dict method"


def test_wall_from_dict_with_minimal_data():
    """Test from_dict with minimal required data."""
    data = {}  # Empty dict, should use defaults

    wall, errors = XmiWall.from_dict(data)
    assert wall is not None
    assert len(errors) == 0
    assert wall.id is not None  # Auto-generated
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_multiple_instances_unique_ids():
    """Test that multiple instances get unique auto-generated IDs."""
    wall1 = XmiWall()
    wall2 = XmiWall()

    assert wall1.id != wall2.id
    assert wall1.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert wall2.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_wall_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    wall = XmiWall(
        id="wall-008",
        name="Inherited Test",
        ifcguid="0987654321FEDCBA",
        native_id="NID-004",
        description="Testing inheritance"
    )

    assert wall.id == "wall-008"
    assert wall.name == "Inherited Test"
    assert wall.ifcguid == "0987654321FEDCBA"
    assert wall.native_id == "NID-004"
    assert wall.description == "Testing inheritance"
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert wall.entity_type == "XmiWall"


def test_wall_different_from_other_entities():
    """Test that wall is different entity type from other physical entities."""
    wall = XmiWall(id="wall-009", name="Compare Test")

    # Same Physical domain
    assert wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    # But different entity type
    assert wall.entity_type == "XmiWall"
    assert wall.entity_type != "XmiBeam"
    assert wall.entity_type != "XmiColumn"
    assert wall.entity_type != "XmiSlab"


def test_wall_equality_based_on_id():
    """Test that walls with same ID are considered different instances."""
    wall1 = XmiWall(id="wall-010", name="Wall A")
    wall2 = XmiWall(id="wall-010", name="Wall B")

    # Different instances even with same ID
    assert wall1 is not wall2
    # But have same ID
    assert wall1.id == wall2.id


def test_wall_partition_vs_structural():
    """Test that description can distinguish partition from structural walls."""
    partition_wall = XmiWall(
        id="wall-011",
        name="Partition Wall",
        description="Non-load-bearing partition"
    )
    structural_wall = XmiWall(
        id="wall-012",
        name="Structural Wall",
        description="Load-bearing shear wall"
    )

    assert partition_wall.description == "Non-load-bearing partition"
    assert structural_wall.description == "Load-bearing shear wall"
    # Both are Physical domain and XmiWall entity type
    assert partition_wall.type == structural_wall.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert partition_wall.entity_type == structural_wall.entity_type == "XmiWall"


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_wall.py
