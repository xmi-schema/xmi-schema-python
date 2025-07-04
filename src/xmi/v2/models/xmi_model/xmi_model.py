from __future__ import annotations

from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_relationship import XmiBaseRelationship
from xmi.v2.utils.xmi_entity_type_mapping import ENTITY_CLASS_MAPPING, RELATIONSHIP_CLASS_MAPPING


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

    def find_entity(self, entity_id: str) -> Optional[XmiBaseEntity]:
        for entity in self.entities:
            if getattr(entity, 'id', None) == entity_id:
                return entity
        return None

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        self.name = data.get("Name")
        self.xmi_version = data.get("XmiVersion")
        self.application_name = data.get("ApplicationName")
        self.application_version = data.get("ApplicationVersion")

        for index, entity_data in enumerate(data.get("Entities", [])):
            entity_type = entity_data.get("EntityType")
            entity_class = ENTITY_CLASS_MAPPING.get(entity_type)

            if not entity_type or not entity_class:
                self.errors.append(ErrorLog(
                    entity_type=entity_type or "Unknown",
                    index=index,
                    message=f"Entity type '{entity_type}' is not recognized.",
                    obj=str(entity_data)
                ))
                continue

            try:
                instance, errors = (entity_class.from_dict(entity_data)
                                    if hasattr(entity_class, 'from_dict')
                                    else (entity_class.model_validate(entity_data), []))
                if instance:
                    self.entities.append(instance)
                self.errors.extend(errors)
            except Exception as e:
                self.errors.append(ErrorLog(
                    entity_type=entity_type,
                    index=index,
                    message=f"Failed to instantiate entity: {str(e)}",
                    obj=str(entity_data)
                ))

        for index, rel_data in enumerate(data.get("Relationships", [])):
            rel_type = rel_data.get("EntityType")
            rel_class = RELATIONSHIP_CLASS_MAPPING.get(rel_type)

            if not rel_type or not rel_class:
                self.errors.append(ErrorLog(
                    entity_type=rel_type or "Unknown",
                    index=index,
                    message=f"Relationship type '{rel_type}' is not recognized.",
                    obj=str(rel_data)
                ))
                continue

            source_id = rel_data.get("Source")
            target_id = rel_data.get("Target")

            source_entity = self.find_entity(source_id)
            target_entity = self.find_entity(target_id)

            if not source_entity or not target_entity:
                self.errors.append(ErrorLog(
                    entity_type=rel_type,
                    index=index,
                    message="Missing source or target entity for relationship.",
                    obj=str(rel_data)
                ))
                continue

            try:
                rel_data_clean = {k: v for k, v in rel_data.items() if k not in ('Source', 'Target')}
                relationship_instance = rel_class(source=source_entity, target=target_entity, **rel_data_clean)
                self.relationships.append(relationship_instance)
            except Exception as e:
                self.errors.append(ErrorLog(
                    entity_type=rel_type,
                    index=index,
                    message=f"Failed to instantiate relationship: {str(e)}",
                    obj=str(rel_data)
                ))