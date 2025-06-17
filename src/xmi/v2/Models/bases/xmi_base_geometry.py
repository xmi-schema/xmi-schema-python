from pydantic import Field, model_validator
from typing import Optional
from .xmi_base_entity import XmiBaseEntity

class XmiBaseGeometry(XmiBaseEntity):
    entity_type: Optional[str] = Field(None, alias="EntityType")

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values["EntityType"] = values.get("EntityType") or values.get("entity_type") or cls.__name__

        return values

    class Config:
        populate_by_name = True


# Testing run python -m src.xmi.v2.models.bases.xmi_base_geometry

geometry = XmiBaseGeometry(
    ID="001",
    Name=None,
    IFCGUID="abc-123",
    Description="Test geometry"
)

print(geometry.model_dump(by_alias=True, exclude_none=True))