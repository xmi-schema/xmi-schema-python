"""
Tests for XmiBaseStructuralAnalyticalEntity base class.

This module tests the abstract base class for all structural analytical entities,
verifying that:
- entity_type is automatically set to "StructuralAnalytical"
- All inherited properties from XmiBaseEntity work correctly
- Proper validation and model behavior
"""

import pytest
from pydantic import ValidationError
from xmi.v2.models.bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity
from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum


# Create a concrete test class since XmiBaseStructuralAnalyticalEntity is abstract
class TestStructuralAnalyticalEntity(XmiBaseStructuralAnalyticalEntity):
    """Concrete implementation for testing purposes."""
    pass


def test_domain_type_auto_assignment():
    """Test that domain type is automatically set to 'StructuralAnalytical'."""
    entity = TestStructuralAnalyticalEntity()
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.entity_type == "TestStructuralAnalyticalEntity"  # Class name


def test_domain_type_with_explicit_id():
    """Test domain type assignment when ID is provided."""
    entity = TestStructuralAnalyticalEntity(id="test-001", name="Test Entity")
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.entity_type == "TestStructuralAnalyticalEntity"
    assert entity.id == "test-001"
    assert entity.name == "Test Entity"


def test_domain_type_not_overridden():
    """Test that domain type is set to 'StructuralAnalytical' even if not provided."""
    entity = TestStructuralAnalyticalEntity(
        id="test-002",
        name="Test Entity 2",
        description="A test structural analytical entity"
    )
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.entity_type == "TestStructuralAnalyticalEntity"


def test_inherited_properties():
    """Test that all properties from XmiBaseEntity are inherited."""
    entity = TestStructuralAnalyticalEntity(
        id="anal-001",
        name="Analytical Entity",
        ifcguid="3cJh8fHxj3FwU$9vPQK1PN",
        native_id="200",
        description="Test analytical entity"
    )

    assert entity.id == "anal-001"
    assert entity.name == "Analytical Entity"
    assert entity.ifcguid == "3cJh8fHxj3FwU$9vPQK1PN"
    assert entity.native_id == "200"
    assert entity.description == "Test analytical entity"
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.entity_type == "TestStructuralAnalyticalEntity"


def test_default_id_generation():
    """Test that ID is auto-generated when not provided."""
    entity = TestStructuralAnalyticalEntity()
    assert entity.id is not None
    assert len(entity.id) > 0
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_name_defaults_to_id():
    """Test that name defaults to ID when not provided."""
    entity = TestStructuralAnalyticalEntity(id="test-id-456")
    assert entity.name == "test-id-456"
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_optional_fields():
    """Test that optional fields can be None."""
    entity = TestStructuralAnalyticalEntity(id="test-003")
    assert entity.ifcguid is None
    assert entity.native_id is None
    assert entity.description is None
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_model_serialization():
    """Test that the model can be serialized to dict."""
    entity = TestStructuralAnalyticalEntity(
        id="anal-002",
        name="Serialization Test",
        description="Test serialization"
    )

    data = entity.model_dump()
    assert data["id"] == "anal-002"
    assert data["name"] == "Serialization Test"
    assert data["type"] == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_model_deserialization_pascalcase():
    """Test that the model can be created from PascalCase dict."""
    data = {
        "ID": "anal-003",
        "Name": "Deserialization Test",
        "Type": "StructuralAnalytical",
        "Description": "Test deserialization"
    }

    entity = TestStructuralAnalyticalEntity.model_validate(data)
    assert entity.id == "anal-003"
    assert entity.name == "Deserialization Test"
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.description == "Test deserialization"


def test_model_deserialization_snake_case():
    """Test that the model can be created from snake_case dict."""
    data = {
        "id": "anal-004",
        "name": "Snake Case Test",
        "type": "StructuralAnalytical",
        "description": "Test snake_case"
    }

    entity = TestStructuralAnalyticalEntity.model_validate(data)
    assert entity.id == "anal-004"
    assert entity.name == "Snake Case Test"
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_multiple_instances_unique_ids():
    """Test that multiple instances get unique auto-generated IDs."""
    entity1 = TestStructuralAnalyticalEntity()
    entity2 = TestStructuralAnalyticalEntity()

    assert entity1.id != entity2.id
    assert entity1.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity2.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL


def test_different_from_physical_domain_type():
    """Test that StructuralAnalytical is different from Physical domain type."""
    entity = TestStructuralAnalyticalEntity(id="compare-001")
    assert entity.type == XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
    assert entity.type != XmiBaseEntityDomainEnum.PHYSICAL


# Run with: pytest tests/xmi/v2/test_entities/test_xmi_base_structural_analytical_entity.py
