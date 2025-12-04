"""
Tests for XmiBasePhysicalEntity base class.

This module tests the abstract base class for all physical entities,
verifying that:
- entity_type is automatically set to "Physical"
- All inherited properties from XmiBaseEntity work correctly
- Proper validation and model behavior
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.bases.xmi_base_physical_entity import XmiBasePhysicalEntity
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


# Create a concrete test class since XmiBasePhysicalEntity is abstract
class TestPhysicalEntity(XmiBasePhysicalEntity):
    """Concrete implementation for testing purposes."""
    pass


def test_domain_type_auto_assignment():
    """Test that domain type is automatically set to 'Physical'."""
    entity = TestPhysicalEntity()
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity.entity_type == "TestPhysicalEntity"  # Class name


def test_domain_type_with_explicit_id():
    """Test domain type assignment when ID is provided."""
    entity = TestPhysicalEntity(id="test-001", name="Test Entity")
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity.entity_type == "TestPhysicalEntity"
    assert entity.id == "test-001"
    assert entity.name == "Test Entity"


def test_domain_type_not_overridden():
    """Test that domain type is set to 'Physical' even if not provided."""
    entity = TestPhysicalEntity(
        id="test-002",
        name="Test Entity 2",
        description="A test physical entity"
    )
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity.entity_type == "TestPhysicalEntity"


def test_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    entity = TestPhysicalEntity(
        id="phys-001",
        name="Physical Entity",
        ifcguid="3cJh8fHxj3FwU$9vPQK1PN",
        native_id="100",
        description="Test physical entity"
    )

    assert entity.id == "phys-001"
    assert entity.name == "Physical Entity"
    assert entity.ifcguid == "3cJh8fHxj3FwU$9vPQK1PN"
    assert entity.native_id == "100"
    assert entity.description == "Test physical entity"
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity.entity_type == "TestPhysicalEntity"


def test_default_id_generation():
    """Test that ID is auto-generated when not provided."""
    entity = TestPhysicalEntity()
    assert entity.id is not None
    assert len(entity.id) > 0
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_name_defaults_to_id():
    """Test that name defaults to ID when not provided."""
    entity = TestPhysicalEntity(id="test-id-123")
    assert entity.name == "test-id-123"
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_optional_fields():
    """Test that optional fields can be None."""
    entity = TestPhysicalEntity(id="test-003")
    assert entity.ifcguid is None
    assert entity.native_id is None
    assert entity.description is None
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_model_serialization():
    """Test that the model can be serialized to dict."""
    entity = TestPhysicalEntity(
        id="phys-002",
        name="Serialization Test",
        description="Test serialization"
    )

    data = entity.model_dump()
    assert data["id"] == "phys-002"
    assert data["name"] == "Serialization Test"
    assert data["type"] == XmiBaseEntityDomainEnum.PHYSICAL


def test_model_deserialization_pascalcase():
    """Test that the model can be created from PascalCase dict."""
    data = {
        "ID": "phys-003",
        "Name": "Deserialization Test",
        "Type": "Physical",
        "Description": "Test deserialization"
    }

    entity = TestPhysicalEntity.model_validate(data)
    assert entity.id == "phys-003"
    assert entity.name == "Deserialization Test"
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity.description == "Test deserialization"


def test_model_deserialization_snake_case():
    """Test that the model can be created from snake_case dict."""
    data = {
        "id": "phys-004",
        "name": "Snake Case Test",
        "type": "Physical",
        "description": "Test snake_case"
    }

    entity = TestPhysicalEntity.model_validate(data)
    assert entity.id == "phys-004"
    assert entity.name == "Snake Case Test"
    assert entity.type == XmiBaseEntityDomainEnum.PHYSICAL


def test_multiple_instances_unique_ids():
    """Test that multiple instances get unique auto-generated IDs."""
    entity1 = TestPhysicalEntity()
    entity2 = TestPhysicalEntity()

    assert entity1.id != entity2.id
    assert entity1.type == XmiBaseEntityDomainEnum.PHYSICAL
    assert entity2.type == XmiBaseEntityDomainEnum.PHYSICAL


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_base_physical_entity.py
