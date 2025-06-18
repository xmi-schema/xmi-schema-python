from abc import ABC
from pydantic import BaseModel, Field, model_validator
from typing import Optional
import uuid

class XmiBaseEntity(BaseModel, ABC):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="ID")
    name: Optional[str] = Field(None, alias="Name")
    ifcguid: Optional[str] = Field(None, alias="IFCGUID")
    native_id: Optional[str] = Field(None, alias="NativeId")
    description: Optional[str] = Field(None, alias="Description")
    entity_type: Optional[str] = Field(None, alias="EntityType")

    @model_validator(mode="before")
    @classmethod
    def fill_defaults(cls, values: dict):
        id_ = values.get("ID") or values.get("id") or str(uuid.uuid4())

        if "ID" not in values and "id" not in values:
            values["ID"] = id_

        if "Name" not in values and "name" not in values:
            values["Name"] = id_

        if "EntityType" not in values and "entity_type" not in values:
            values["EntityType"] = cls.__name__

        return values

    class Config:
        populate_by_name = True


# Testing run python -m src.xmi.v2.models.bases.xmi_base_entity 

class XmiStructuralMaterial(XmiBaseEntity):
    material_type: str
    unit_weight: Optional[float] = None

    def get_info(self) -> str:
        return f"id: {self.id}, {self.name} ({self.material_type}), weight: {self.unit_weight}"

    def create(self):
        print(f"Creating structural material: {self.name}")

entity = XmiStructuralMaterial(
    name="123",
    ifcguid="ABC123",
    description="Steel beam",
    material_type="Steel",
    unit_weight=78.5
)

print(entity.get_info())
entity.create()