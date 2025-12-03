from abc import ABC, abstractmethod
from typing import Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BaseShapeParameters(BaseModel, ABC):
    """
    Abstract base class for shape parameters.

    This class provides the foundation for all shape-specific parameter classes.
    Each shape parameter class defines the geometric dimensions required for that
    particular cross-section shape.

    The parameters are stored as a dictionary with symbolic keys (H, B, T, etc.)
    mapping to numeric values, following the XMI schema specification.

    Examples:
        >>> # Rectangular shape parameters
        >>> rect_params = RectangularShapeParameters(H=0.5, B=0.3)
        >>> params_dict = rect_params.to_dict()
        >>> print(params_dict)  # {"H": 0.5, "B": 0.3}

    Note:
        This is an abstract base class and cannot be instantiated directly.
        Use concrete subclasses for specific shapes.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

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
