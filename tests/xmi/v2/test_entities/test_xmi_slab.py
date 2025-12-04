"""
Tests for XmiSlab physical entity class.

This module tests the XmiSlab class, verifying that:
- It inherits from XmiBasePhysicalEntity
- Domain type is automatically set to "Physical"
- All inherited properties work correctly
- Serialization and deserialization work correctly
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.entities.physical.xmi_slab import XmiSlab
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


def test_slab_basic_creation():
    """Test basic slab creation."""
    slab = XmiSlab(
        id="slab-001",
        name="Floor Slab 1"
    )

    assert slab.id == "slab-001"
    assert slab.name == "Floor Slab 1"
    assert slab.entity_type == "XmiSlab"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_domain_type_automatic():
    """Test that domain type is automatically set to Physical."""
    slab = XmiSlab()
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert slab.entity_type == "XmiSlab"


def test_slab_with_all_properties():
    """Test slab creation with all inherited properties specified."""
    slab = XmiSlab(
        id="slab-002",
        name="Roof Slab",
        ifcguid="5eL j0hJzl5HyW$1xTSM3QP",
        native_id="67890",
        description="Concrete roof slab"
    )

    assert slab.id == "slab-002"
    assert slab.name == "Roof Slab"
    assert slab.ifcguid == "5eL j0hJzl5HyW$1xTSM3QP"
    assert slab.native_id == "67890"
    assert slab.description == "Concrete roof slab"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert slab.entity_type == "XmiSlab"


def test_slab_default_id_generation():
    """Test that ID is auto-generated when not provided."""
    slab = XmiSlab()
    assert slab.id is not None
    assert len(slab.id) > 0
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_name_defaults_to_id():
    """Test that name defaults to ID when not provided."""
    slab = XmiSlab(id="slab-id-456")
    assert slab.name == "slab-id-456"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_optional_fields():
    """Test that optional fields can be None."""
    slab = XmiSlab(id="slab-003")
    assert slab.ifcguid is None
    assert slab.native_id is None
    assert slab.description is None
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_serialization():
    """Test that slab can be serialized to dict."""
    slab = XmiSlab(
        id="slab-004",
        name="Serialization Test",
        description="Test serialization"
    )

    data = slab.model_dump()
    assert data["id"] == "slab-004"
    assert data["name"] == "Serialization Test"
    assert data["entity_type"] == "XmiSlab"
    assert data["type"] == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_deserialization_pascalcase():
    """Test that slab can be created from PascalCase dict."""
    data = {
        "ID": "slab-005",
        "Name": "Deserialization Test",
        "Type": "Physical",
        "Description": "Test deserialization"
    }

    slab = XmiSlab.model_validate(data)
    assert slab.id == "slab-005"
    assert slab.name == "Deserialization Test"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert slab.description == "Test deserialization"


def test_slab_deserialization_snake_case():
    """Test that slab can be created from snake_case dict."""
    data = {
        "id": "slab-006",
        "name": "Snake Case Test",
        "type": "Physical",
        "description": "Test snake_case"
    }

    slab = XmiSlab.model_validate(data)
    assert slab.id == "slab-006"
    assert slab.name == "Snake Case Test"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_from_dict_method():
    """Test the from_dict class method."""
    data = {
        "ID": "slab-007",
        "Name": "From Dict Test",
        "NativeId": "98765",
        "Description": "Testing from_dict method"
    }

    slab, errors = XmiSlab.from_dict(data)
    assert slab is not None
    assert len(errors) == 0
    assert slab.id == "slab-007"
    assert slab.name == "From Dict Test"
    assert slab.native_id == "98765"
    assert slab.description == "Testing from_dict method"


def test_slab_from_dict_with_minimal_data():
    """Test from_dict with minimal required data."""
    data = {}  # Empty dict, should use defaults

    slab, errors = XmiSlab.from_dict(data)
    assert slab is not None
    assert len(errors) == 0
    assert slab.id is not None  # Auto-generated
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_multiple_instances_unique_ids():
    """Test that multiple instances get unique auto-generated IDs."""
    slab1 = XmiSlab()
    slab2 = XmiSlab()

    assert slab1.id != slab2.id
    assert slab1.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert slab2.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_slab_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    slab = XmiSlab(
        id="slab-008",
        name="Inherited Test",
        ifcguid="ABCDEF1234567890",
        native_id="NID-003",
        description="Testing inheritance"
    )

    assert slab.id == "slab-008"
    assert slab.name == "Inherited Test"
    assert slab.ifcguid == "ABCDEF1234567890"
    assert slab.native_id == "NID-003"
    assert slab.description == "Testing inheritance"
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert slab.entity_type == "XmiSlab"


def test_slab_different_from_beam():
    """Test that slab is different entity type from beam."""
    slab = XmiSlab(id="slab-009", name="Compare Test")

    # Same Physical domain
    assert slab.type == XmiBaseEntityDomainEnum.PHYSICAL
    # But different entity type
    assert slab.entity_type == "XmiSlab"
    assert slab.entity_type != "XmiBeam"
    assert slab.entity_type != "XmiColumn"


def test_slab_equality_based_on_id():
    """Test that slabs with same ID are considered different instances."""
    slab1 = XmiSlab(id="slab-010", name="Slab A")
    slab2 = XmiSlab(id="slab-010", name="Slab B")

    # Different instances even with same ID
    assert slab1 is not slab2
    # But have same ID
    assert slab1.id == slab2.id


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_slab.py
