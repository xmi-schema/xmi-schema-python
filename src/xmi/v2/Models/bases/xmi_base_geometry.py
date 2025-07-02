from pydantic import Field, model_validator, ConfigDict
from typing import Optional
from .xmi_base_entity import XmiBaseEntity

class XmiBaseGeometry(XmiBaseEntity):
    entity_type: Optional[str] = Field(None, alias="EntityType")

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values["EntityType"] = values.get("EntityType") or values.get("entity_type") or cls.__name__

        return values

    model_config = ConfigDict(populate_by_name=True)
