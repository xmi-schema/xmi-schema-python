from abc import ABC
from pydantic import BaseModel, Field, model_validator, ConfigDict
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

    model_config = ConfigDict(populate_by_name=True)
