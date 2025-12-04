from pydantic import Field, field_validator, model_validator, ConfigDict, field_serializer
from typing import Dict, Any, List, Optional, Tuple, Union
from ...bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity
from ...enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from ...enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from ....utils.xmi_errors import *
from ....utils.xmi_utilities import *

class XmiStructuralCurveMember(XmiBaseStructuralAnalyticalEntity):
    curve_member_type: XmiStructuralCurveMemberTypeEnum = Field(..., alias="CurveMemberType")
    system_line: XmiStructuralCurveMemberSystemLineEnum = Field(..., alias="SystemLine")

    local_axis_x: Tuple[float, float, float] = Field((1.0, 0.0, 0.0), alias="LocalAxisX")
    local_axis_y: Tuple[float, float, float] = Field((0.0, 1.0, 0.0), alias="LocalAxisY")
    local_axis_z: Tuple[float, float, float] = Field((0.0, 0.0, 1.0), alias="LocalAxisZ")

    begin_node_x_offset: float = Field(0.0, alias="BeginNodeXOffset")
    end_node_x_offset: float = Field(0.0, alias="EndNodeXOffset")
    begin_node_y_offset: float = Field(0.0, alias="BeginNodeYOffset")
    end_node_y_offset: float = Field(0.0, alias="EndNodeYOffset")
    begin_node_z_offset: float = Field(0.0, alias="BeginNodeZOffset")
    end_node_z_offset: float = Field(0.0, alias="EndNodeZOffset")

    length: Optional[Union[int, float]] = Field(None, alias="Length")

    end_fixity_start: Optional[str] = Field(None, alias="EndFixityStart")
    end_fixity_end: Optional[str] = Field(None, alias="EndFixityEnd")

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
        values.setdefault("EntityType", "XmiStructuralCurveMember")
        return values

    @field_serializer("local_axis_x", "local_axis_y", "local_axis_z", when_used="json")
    def serialize_axes(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        try:
            coords = tuple(float(v) for v in value)
        except TypeError:
            return value
        return ",".join(f"{coord:g}" for coord in coords)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiStructuralCurveMember"], List[Exception]]:
        errors = []
        processed = obj.copy()

        try:
            processed["system_line"] = XmiStructuralCurveMemberSystemLineEnum.from_attribute_get_enum(
                processed["SystemLine"]
            )
        except Exception as e:
            errors.append(e)

        try:
            processed["curve_member_type"] = XmiStructuralCurveMemberTypeEnum.from_attribute_get_enum(
                processed["CurveMemberType"]
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
