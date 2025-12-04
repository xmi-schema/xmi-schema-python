from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional
from ..bases.xmi_base_relationship import XmiBaseRelationship
from ..bases.xmi_base_entity import XmiBaseEntity
from ..entities.structural_analytical.xmi_structural_point_connection import XmiStructuralPointConnection

class XmiHasStructuralPointConnection(XmiBaseRelationship):
    is_begin: Optional[bool] = Field(None, alias="IsBegin")
    is_end: Optional[bool] = Field(None, alias="IsEnd")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, v):
        if not isinstance(v, XmiBaseEntity):
            raise TypeError("Source should be of type XmiBaseEntity")
        return v

    @field_validator("target", mode="before")
    @classmethod
    def validate_target(cls, v):
        if not isinstance(v, XmiStructuralPointConnection):
            raise TypeError("Target should be of type XmiStructuralPointConnection")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        values.setdefault("name", "hasStructuralPointConnection")
        values.setdefault("entity_type", "XmiRelHasStructuralPointConnection")
        return values
