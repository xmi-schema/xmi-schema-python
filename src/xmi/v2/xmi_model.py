from __future__ import annotations
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_relationship import XmiBaseRelationship
from xmi.v2.utils.xmi_entity_type_mapping import ENTITY_TYPE_MAPPING


class ErrorLog(BaseModel):
    entity_type: str = Field(..., alias="EntityType")
    index: int = Field(..., alias="Index")
    message: str = Field(..., alias="Message")
    obj: Optional[str] = Field(None, alias="Obj")

    model_config = ConfigDict(populate_by_name=True)


class XmiModel(BaseModel):
    entities: List[XmiBaseEntity] = Field(default_factory=list, alias="Entities")
    relationships: List[XmiBaseRelationship] = Field(default_factory=list, alias="Relationships")
    histories: List[dict] = Field(default_factory=list, alias="Histories")
    errors: List[ErrorLog] = Field(default_factory=list, alias="Errors")

    name: Optional[str] = Field(None, alias="Name")
    xmi_version: Optional[str] = Field(None, alias="XmiVersion")
    application_name: Optional[str] = Field(None, alias="ApplicationName")
    application_version: Optional[str] = Field(None, alias="ApplicationVersion")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator('name', 'xmi_version', 'application_name', 'application_version', mode="before")
    @classmethod
    def validate_strings(cls, v):
        if v is not None and not isinstance(v, str):
            raise TypeError("Value must be a string or None")
        return v

    @model_validator(mode="before")
    @classmethod
    def instantiate_entities(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        entities = values.get("Entities", [])
        instantiated_entities = []

        for entity_dict in entities:
            entity_type = entity_dict.get("EntityType")
            entity_class = ENTITY_TYPE_MAPPING.get(entity_type)

            if entity_class and hasattr(entity_class, "from_dict"):
                instance, errors = entity_class.from_dict(entity_dict)
                if instance:
                    instantiated_entities.append(instance)
                else:
                    instantiated_entities.append(entity_dict)
            elif entity_class:
                try:
                    instance = entity_class.model_validate(entity_dict)
                    instantiated_entities.append(instance)
                except Exception:
                    instantiated_entities.append(entity_dict)
            else:
                instantiated_entities.append(entity_dict)

        values["Entities"] = instantiated_entities
        return values

    def create_relationship(
        self,
        relationship_class: Type[XmiBaseRelationship],
        source: XmiBaseEntity,
        target: XmiBaseEntity,
        name: Optional[str] = None,
        **kwargs
    ) -> XmiBaseRelationship:

        if relationship_class == XmiBaseRelationship:
            relationship = relationship_class(source=source, target=target, name=name)
        else:
            relationship = relationship_class(source=source, target=target, **kwargs)

        self.relationships.append(relationship)
        return relationship

    def find_relationships_by_target(self, target: XmiBaseEntity) -> List[XmiBaseRelationship]:
        return [rel for rel in self.relationships if rel.target == target]

    def find_relationships_by_source(self, source: XmiBaseEntity) -> List[XmiBaseRelationship]:
        return [rel for rel in self.relationships if rel.source == source]