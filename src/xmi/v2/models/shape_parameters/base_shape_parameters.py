from abc import ABC, abstractmethod
from typing import Dict, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from ..enums.xmi_unit_enum import XmiUnitEnum


class BaseShapeParameters(BaseModel, ABC):
    """
    Abstract base class for shape parameters.

    This class provides the foundation for all shape-specific parameter classes.
    Each shape parameter class defines the geometric dimensions required for that
    particular cross-section shape.

    The parameters are stored as a dictionary with symbolic keys (H, B, T, etc.)
    mapping to numeric values, following the XMI schema specification.

    Attributes:
        unit: Optional unit of measurement for the parameters (default: MILLIMETER)

    Examples:
        >>> # Rectangular shape parameters with default mm unit
        >>> rect_params = RectangularShapeParameters(H=500, B=300)
        >>> params_dict = rect_params.to_dict()
        >>> print(params_dict)  # {"H": 500, "B": 300}
        >>> print(rect_params.unit)  # XmiUnitEnum.MILLIMETER

        >>> # Rectangular shape parameters with explicit unit
        >>> from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
        >>> rect_params = RectangularShapeParameters(H=0.5, B=0.3, unit=XmiUnitEnum.METER)
        >>> print(rect_params.unit)  # XmiUnitEnum.METER

    Note:
        This is an abstract base class and cannot be instantiated directly.
        Use concrete subclasses for specific shapes.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    # Unit field - optional, defaults to MILLIMETER
    unit: Optional["XmiUnitEnum"] = Field(None, description="Unit of measurement for parameters")

    @abstractmethod
    def to_dict(self) -> Dict[str, float]:
        """
        Convert shape parameters to dictionary format.

        Returns:
            Dict[str, float]: Dictionary mapping parameter symbols to values

        Examples:
            >>> params = RectangularShapeParameters(H=0.5, B=0.3)
            >>> params.to_dict()
            {"H": 0.5, "B": 0.3}
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, float]) -> "BaseShapeParameters":
        """
        Create shape parameters from dictionary.

        Args:
            data: Dictionary mapping parameter symbols to values

        Returns:
            BaseShapeParameters: Instance of the shape parameters class

        Examples:
            >>> data = {"H": 0.5, "B": 0.3}
            >>> params = RectangularShapeParameters.from_dict(data)
        """
        pass

    def _validate_positive(self, value: float, field_name: str) -> float:
        """Validate that a value is positive."""
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0, got {value}")
        return value

    def _validate_non_negative(self, value: float, field_name: str) -> float:
        """Validate that a value is non-negative."""
        if value < 0:
            raise ValueError(f"{field_name} must be non-negative, got {value}")
        return value

    def convert_to(self, target_unit: "XmiUnitEnum") -> "BaseShapeParameters":
        """
        Convert shape parameters to a different unit.

        Args:
            target_unit: The target unit to convert to

        Returns:
            BaseShapeParameters: New instance with converted values

        Raises:
            ValueError: If current unit is not set or conversion is invalid

        Examples:
            >>> from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
            >>> params = RectangularShapeParameters(H=500, B=300, unit=XmiUnitEnum.MILLIMETER)
            >>> params_m = params.convert_to(XmiUnitEnum.METER)
            >>> print(params_m.H, params_m.B)  # 0.5, 0.3
        """
        from ...utils.xmi_unit_conversion import convert_dict

        if self.unit is None:
            raise ValueError("Cannot convert parameters without a unit specified")

        if self.unit == target_unit:
            return self.model_copy()

        # Get parameter dict and convert
        params_dict = self.to_dict()
        converted_dict = convert_dict(params_dict, self.unit, target_unit)

        # Create new instance with converted values
        new_instance = self.from_dict(converted_dict)
        new_instance.unit = target_unit

        return new_instance

    def get_unit_display_string(self) -> str:
        """
        Get a display string for the unit.

        Returns:
            str: Unit display string (e.g., "mm", "in", "m")

        Examples:
            >>> from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
            >>> params = RectangularShapeParameters(H=500, B=300, unit=XmiUnitEnum.MILLIMETER)
            >>> params.get_unit_display_string()
            'mm'
        """
        if self.unit is None:
            return "mm"  # Default
        return self.unit.value
