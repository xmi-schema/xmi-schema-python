from __future__ import annotations

import inspect
from typing import Dict, Any, List, Optional, Type, Callable, Tuple
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, PrivateAttr
from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_relationship import XmiBaseRelationship
from xmi.v2.utils.xmi_entity_type_mapping import ENTITY_CLASS_MAPPING, RELATIONSHIP_CLASS_MAPPING
from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D


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
    _point_cache: Dict[Tuple[int, int, int, float], XmiPoint3D] = PrivateAttr(default_factory=dict)
    _point_tolerance: float = PrivateAttr(default=1e-10)

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

    def _quantize(self, value: float, tolerance: float) -> int:
        return round(value / tolerance)

    def _point_cache_key(self, x: float, y: float, z: float, tolerance: float) -> Tuple[int, int, int, float]:
        return (
            self._quantize(x, tolerance),
            self._quantize(y, tolerance),
            self._quantize(z, tolerance),
            tolerance,
        )

    def _register_point(self, point: XmiPoint3D, tolerance: Optional[float] = None) -> None:
        tol = tolerance if tolerance is not None else self._point_tolerance
        key = self._point_cache_key(point.x, point.y, point.z, tol)
        self._point_cache[key] = point

    def create_point_3d(self, x: float, y: float, z: float, tolerance: Optional[float] = None) -> XmiPoint3D:
        """Factory that reuses coordinates already present in the model within tolerance."""
        tol = tolerance if tolerance is not None else self._point_tolerance
        key = self._point_cache_key(x, y, z, tol)
        cached = self._point_cache.get(key)
        if cached and (
            abs(cached.x - x) <= tol and
            abs(cached.y - y) <= tol and
            abs(cached.z - z) <= tol
        ):
            return cached

        candidate = XmiPoint3D(x=x, y=y, z=z)
        self._point_cache[key] = candidate
        return candidate

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
                from_dict_kwargs = {}
                if hasattr(entity_class, 'from_dict'):
                    params = inspect.signature(entity_class.from_dict).parameters
                    if 'point_factory' in params:
                        from_dict_kwargs['point_factory'] = self.create_point_3d
                    instance, errors = entity_class.from_dict(entity_data, **from_dict_kwargs)
                else:
                    instance = entity_class.model_validate(entity_data)
                    errors = []
                if instance:
                    self.entities.append(instance)
                    if isinstance(instance, XmiPoint3D):
                        self._register_point(instance)
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
