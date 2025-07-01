from pydantic import Field, field_validator, model_validator
from typing import Dict, Any, List, Optional, Tuple, Union
from ..bases.xmi_base_entity import XmiBaseEntity
from ..enums.xmi_structural_curve_member_type_enum import XmiStructuralCurveMemberTypeEnum
from ..enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from ...utils.xmi_errors import *
from ...utils.xmi_utilities import *

class XmiStructuralCurveMember(XmiBaseEntity):
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

    end_fixity_start: Optional[float]  = Field(None, alias="EndFixityStart")
    end_fixity_end: Optional[float] = Field(None, alias="EndFixityEnd")

    model_config = {
        "populate_by_name": True,
    }


    @field_validator("local_axis_x", "local_axis_y", "local_axis_z", mode="before")
    @classmethod
    def parse_and_validate_axis(cls, v, info):
        if isinstance(v, tuple):
            if len(v) != 3 or not all(isinstance(i, (int, float)) for i in v):
                raise ValueError(f"{info.field_name} must be a tuple of 3 numbers")
            return tuple(float(i) for i in v)

        if isinstance(v, str):
            parts = v.split(',')
            if len(parts) != 3:
                raise ValueError(f"{info.field_name} must contain exactly 3 components separated by commas")
            try:
                return tuple(float(part.strip()) for part in parts)
            except ValueError as e:
                raise ValueError(f"All values in {info.field_name} must be valid numbers") from e

        raise TypeError(f"{info.field_name} must be a string or tuple of 3 numbers")


    @model_validator(mode="before")
    @classmethod
    def fill_entity_type(cls, values):
        values.setdefault("EntityType", "XmiStructuralCurveMember")
        return values
    

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
                processed["CurvememberType"]
            )
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_x"] = cls.parse_and_validate_axis("x", processed["LocalAxisX"])
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_y"] = cls.parse_and_validate_axis("y", processed["LocalAxisY"])
        except Exception as e:
            errors.append(e)

        try:
            processed["local_axis_z"] = cls.parse_and_validate_axis("z", processed["LocalAxisZ"])
        except Exception as e:
            errors.append(e)

        if errors:
            return None, errors

        try:
            instance = cls(**processed)
            return instance, []
        except Exception as e:
            return None, [e]

