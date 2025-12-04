from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Dict, Any, List, Optional, Tuple, Union
from ...bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity
from ...enums.xmi_structural_surface_member_type_enum import XmiStructuralSurfaceMemberTypeEnum
from ...enums.xmi_structural_surface_member_system_plane_enum import XmiStructuralSurfaceMemberSystemPlaneEnum
from ....utils.xmi_errors import *

class XmiStructuralSurfaceMember(XmiBaseStructuralAnalyticalEntity):
    surface_member_type: XmiStructuralSurfaceMemberTypeEnum = Field(..., alias="SurfaceMemberType")
    thickness: Union[float, int] = Field(..., alias="Thickness")
    system_plane: XmiStructuralSurfaceMemberSystemPlaneEnum = Field(..., alias="SystemPlane")
    area: Optional[Union[float, int]] = Field(None, alias="Area")
    z_offset: Union[float, int] = Field(0.0, alias="ZOffset")
    local_axis_x: Tuple[float, float, float] = Field((1.0, 0.0, 0.0), alias="LocalAxisX")
    local_axis_y: Tuple[float, float, float] = Field((0.0, 1.0, 0.0), alias="LocalAxisY")
    local_axis_z: Tuple[float, float, float] = Field((0.0, 0.0, 1.0), alias="LocalAxisZ")
    height: Optional[Union[float, int]] = Field(None, alias="Height")

    model_config = ConfigDict(populate_by_name=True)

    @staticmethod
    def parse_axis_string(value: Union[str, Tuple]) -> Tuple[float, float, float]:
        if isinstance(value, tuple):
            if len(value) != 3 or not all(isinstance(i, (int, float)) for i in value):
                raise ValueError("Axis tuple must contain exactly 3 numbers")
            return tuple(float(i) for i in value)

        if isinstance(value, str):
            parts = value.split(",")
            if len(parts) != 3:
                raise ValueError("Axis string must contain exactly 3 comma-separated values")
            try:
                return tuple(float(p.strip()) for p in parts)
            except ValueError as e:
                raise ValueError("All axis values must be valid numbers") from e

        raise TypeError("Axis must be a string or tuple of 3 floats")

    @field_validator("local_axis_x", "local_axis_y", "local_axis_z", mode="before")
    @classmethod
    def parse_and_validate_axis(cls, v, info):
        return cls.parse_axis_string(v)

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("EntityType", cls.__name__)
        return values
    
    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiStructuralSurfaceMember"], List[Exception]]:
        errors: List[Exception] = []
        processed = obj.copy()

        try:
            processed["surface_member_type"] = XmiStructuralSurfaceMemberTypeEnum.from_attribute_get_enum(
                processed["SurfaceMemberType"]
            )
        except Exception as e:
            errors.append(e)

        try:
            processed["system_plane"] = XmiStructuralSurfaceMemberSystemPlaneEnum.from_attribute_get_enum(
                processed["SystemPlane"]
            )
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_x"] = cls.parse_axis_string(processed["LocalAxisX"])
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_y"] = cls.parse_axis_string(processed["LocalAxisY"])
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_z"] = cls.parse_axis_string(processed["LocalAxisZ"])
        except Exception as e:
            errors.append(e)

        if errors:
            return None, errors

        try:
            instance = cls(**processed)
            return instance, []
        except Exception as e:
            return None, [e]
    