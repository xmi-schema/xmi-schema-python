from pydantic import BaseModel, Field, model_validator, ConfigDict
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
        if not values.get("name"):
            raise ValueError("Name must be provided")
        return values

    model_config = ConfigDict(populate_by_name=True)