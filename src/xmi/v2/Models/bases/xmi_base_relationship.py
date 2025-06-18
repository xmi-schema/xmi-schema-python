from pydantic import BaseModel, Field, model_validator
from typing import Optional
from .xmi_base_entity import XmiBaseEntity 
import uuid


class XmiBaseRelationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="ID")
    source: XmiBaseEntity = Field(..., alias="Source", description="Source entity")
    target: XmiBaseEntity = Field(..., alias="Target", description="Target entity")
    name: str = Field(..., alias="Name", description="Relationship name")
    description: Optional[str] = Field("", alias="Description")
    entity_type: str = Field(default="XmiRelBaseRelationship", alias="EntityType")
    uml_type: Optional[str] = Field("", alias="UmlType")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values):
        if not isinstance(values.get("source"), XmiBaseEntity):
            raise TypeError("Source must be of type XmiBaseEntity")
        if not isinstance(values.get("target"), XmiBaseEntity):
            raise TypeError("Target must be of type XmiBaseEntity")
        if not values.get("name"):
            raise ValueError("Name must be provided")
        return values

    class Config:
        populate_by_name = True


# Testing run python -m src.xmi.v2.models.bases.xmi_base_relationship

source = XmiBaseEntity(id="123", name="StartNode", entity_type="Node")
target = XmiBaseEntity(id="456", name="EndNode", entity_type="Node")

relationship = XmiBaseRelationship(source=source, target=target, name="connects_to")

print(relationship.model_dump(by_alias=True, exclude_none=True))