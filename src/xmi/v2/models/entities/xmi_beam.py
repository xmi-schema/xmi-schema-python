from pydantic import Field, field_validator, model_validator, ConfigDict, field_serializer
from typing import Dict, Any, List, Optional, Tuple, Union
from ..bases.xmi_base_physical_entity import XmiBasePhysicalEntity
from ..enums.xmi_structural_curve_member_system_line_enum import XmiStructuralCurveMemberSystemLineEnum
from ...utils.xmi_errors import *


class XmiBeam(XmiBasePhysicalEntity):
    """
    Represents a physical beam element in the XMI schema.

    A beam is a horizontal or inclined structural member designed to resist loads
    primarily through bending. This class inherits from XmiBasePhysicalEntity and
    is automatically classified with type (domain) = "Physical".

    Attributes:
        system_line: The reference line of the beam within its cross-section
        length: The length of the beam
        local_axis_x: Local X-axis direction as (x, y, z) tuple
        local_axis_y: Local Y-axis direction as (x, y, z) tuple
        local_axis_z: Local Z-axis direction as (x, y, z) tuple
        begin_node_x_offset: X offset at the beginning node (default: 0.0)
        end_node_x_offset: X offset at the end node (default: 0.0)
        begin_node_y_offset: Y offset at the beginning node (default: 0.0)
        end_node_y_offset: Y offset at the end node (default: 0.0)
        begin_node_z_offset: Z offset at the beginning node (default: 0.0)
        end_node_z_offset: Z offset at the end node (default: 0.0)
        end_fixity_start: Fixity condition at the start of the beam
        end_fixity_end: Fixity condition at the end of the beam
    """

    system_line: XmiStructuralCurveMemberSystemLineEnum = Field(..., alias="SystemLine")
    length: Union[float, int] = Field(..., alias="Length")

    local_axis_x: Tuple[float, float, float] = Field((1.0, 0.0, 0.0), alias="LocalAxisX")
    local_axis_y: Tuple[float, float, float] = Field((0.0, 1.0, 0.0), alias="LocalAxisY")
    local_axis_z: Tuple[float, float, float] = Field((0.0, 0.0, 1.0), alias="LocalAxisZ")

    begin_node_x_offset: float = Field(0.0, alias="BeginNodeXOffset")
    end_node_x_offset: float = Field(0.0, alias="EndNodeXOffset")
    begin_node_y_offset: float = Field(0.0, alias="BeginNodeYOffset")
    end_node_y_offset: float = Field(0.0, alias="EndNodeYOffset")
    begin_node_z_offset: float = Field(0.0, alias="BeginNodeZOffset")
    end_node_z_offset: float = Field(0.0, alias="EndNodeZOffset")

    end_fixity_start: Optional[str] = Field(None, alias="EndFixityStart")
    end_fixity_end: Optional[str] = Field(None, alias="EndFixityEnd")

    model_config = ConfigDict(populate_by_name=True)

    @staticmethod
    def parse_axis_string(value: Union[str, Tuple]) -> Tuple[float, float, float]:
        """
        Parse an axis value from either a string or tuple format.

        Args:
            value: Either a string like "1.0, 0.0, 0.0" or a tuple (1.0, 0.0, 0.0)

        Returns:
            Tuple of three floats representing the axis direction

        Raises:
            ValueError: If the value format is invalid
            TypeError: If the value is not a string or tuple
        """
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
        """Validate and parse axis values before model creation."""
        return cls.parse_axis_string(v)

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        """Set entity_type to class name if not already set."""
        values.setdefault("EntityType", cls.__name__)
        return values

    @field_serializer("local_axis_x", "local_axis_y", "local_axis_z", when_used="json")
    def serialize_axes(self, value):
        """Emit axis directions using the comma-separated string format expected by C#."""
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
    def from_dict(cls, obj: Dict[str, Any]) -> Tuple[Optional["XmiBeam"], List[Exception]]:
        """
        Create an XmiBeam instance from a dictionary, collecting any errors.

        Args:
            obj: Dictionary containing beam data with PascalCase keys

        Returns:
            Tuple of (XmiBeam instance or None, list of exceptions)
        """
        errors: List[Exception] = []
        processed = obj.copy()

        try:
            processed["system_line"] = XmiStructuralCurveMemberSystemLineEnum.from_attribute_get_enum(
                processed["SystemLine"]
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
