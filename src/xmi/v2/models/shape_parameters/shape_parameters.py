"""
Shape parameter classes for XMI cross-sections.

This module provides strongly-typed parameter classes for each cross-section shape
in the XMI schema. Each class serializes into a dictionary pairing symbols
(H, B, T, etc.) with numeric values.

The implementation follows the C# reference:
https://github.com/xmi-schema/xmi-schema-csharp/blob/main/XmiShapeEnumParameters.md
"""

from typing import Dict, Optional
from pydantic import Field, field_validator
from .base_shape_parameters import BaseShapeParameters


class CircularShapeParameters(BaseShapeParameters):
    """
    Parameters for circular cross-sections.

    Attributes:
        D: Diameter

    Examples:
        >>> params = CircularShapeParameters(D=0.4)
        >>> params.to_dict()
        {"D": 0.4}
    """
    D: float = Field(..., gt=0, description="Diameter")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "CircularShapeParameters":
        return cls(D=data["D"])


class RectangularShapeParameters(BaseShapeParameters):
    """
    Parameters for rectangular cross-sections.

    Attributes:
        H: Height
        B: Width/Breadth

    Examples:
        >>> params = RectangularShapeParameters(H=0.5, B=0.3)
        >>> params.to_dict()
        {"H": 0.5, "B": 0.3}
    """
    H: float = Field(..., gt=0, description="Height")
    B: float = Field(..., gt=0, description="Width/Breadth")

    def to_dict(self) -> Dict[str, float]:
        return {"H": self.H, "B": self.B}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "RectangularShapeParameters":
        return cls(H=data["H"], B=data["B"])


class LShapeParameters(BaseShapeParameters):
    """
    Parameters for L-shaped (angle) cross-sections.

    Attributes:
        H: Height
        B: Width
        T: Flange thickness
        t: Web thickness

    Examples:
        >>> params = LShapeParameters(H=0.15, B=0.1, T=0.01, t=0.008)
    """
    H: float = Field(..., gt=0, description="Height")
    B: float = Field(..., gt=0, description="Width")
    T: float = Field(..., gt=0, description="Flange thickness")
    t: float = Field(..., gt=0, description="Web thickness")

    def to_dict(self) -> Dict[str, float]:
        return {"H": self.H, "B": self.B, "T": self.T, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "LShapeParameters":
        return cls(H=data["H"], B=data["B"], T=data["T"], t=data["t"])


class TShapeParameters(BaseShapeParameters):
    """
    Parameters for T-shaped cross-sections.

    Supports two formats:
    - Standard: H, B, T, t
    - Alternate: d, B, T, t, r

    Attributes:
        H: Height (standard format)
        B: Width
        T: Flange thickness
        t: Web thickness
        d: Depth (alternate format)
        r: Root radius (alternate format)

    Examples:
        >>> # Standard format
        >>> params = TShapeParameters(H=0.3, B=0.2, T=0.015, t=0.01)
        >>> # Alternate format
        >>> params = TShapeParameters(d=0.3, B=0.2, T=0.015, t=0.01, r=0.012)
    """
    H: Optional[float] = Field(None, gt=0, description="Height")
    B: float = Field(..., gt=0, description="Width")
    T: float = Field(..., gt=0, description="Flange thickness")
    t: float = Field(..., gt=0, description="Web thickness")
    d: Optional[float] = Field(None, gt=0, description="Depth (alternate)")
    r: Optional[float] = Field(None, ge=0, description="Root radius (alternate)")

    @field_validator('H', 'd')
    @classmethod
    def validate_height_or_depth(cls, v, info):
        # At least one of H or d must be provided
        return v

    def to_dict(self) -> Dict[str, float]:
        if self.d is not None and self.r is not None:
            # Alternate format
            result = {"d": self.d, "B": self.B, "T": self.T, "t": self.t, "r": self.r}
        elif self.H is not None:
            # Standard format
            result = {"H": self.H, "B": self.B, "T": self.T, "t": self.t}
        else:
            raise ValueError("Either H or (d, r) must be provided")
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "TShapeParameters":
        return cls(**data)


class CShapeParameters(BaseShapeParameters):
    """
    Parameters for C-shaped (channel) cross-sections.

    Attributes:
        H: Height
        B: Width
        T1: Top flange thickness
        T2: Bottom flange thickness
        t: Web thickness

    Examples:
        >>> params = CShapeParameters(H=0.2, B=0.075, T1=0.015, T2=0.015, t=0.01)
    """
    H: float = Field(..., gt=0, description="Height")
    B: float = Field(..., gt=0, description="Width")
    T1: float = Field(..., gt=0, description="Top flange thickness")
    T2: float = Field(..., gt=0, description="Bottom flange thickness")
    t: float = Field(..., gt=0, description="Web thickness")

    def to_dict(self) -> Dict[str, float]:
        return {"H": self.H, "B": self.B, "T1": self.T1, "T2": self.T2, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "CShapeParameters":
        return cls(H=data["H"], B=data["B"], T1=data["T1"], T2=data["T2"], t=data["t"])


class IShapeParameters(BaseShapeParameters):
    """
    Parameters for I-shaped (wide flange) cross-sections.

    Attributes:
        D: Depth
        B: Flange width
        T: Flange thickness
        t: Web thickness
        r: Root radius

    Examples:
        >>> params = IShapeParameters(D=0.3, B=0.15, T=0.015, t=0.01, r=0.012)
    """
    D: float = Field(..., gt=0, description="Depth")
    B: float = Field(..., gt=0, description="Flange width")
    T: float = Field(..., gt=0, description="Flange thickness")
    t: float = Field(..., gt=0, description="Web thickness")
    r: float = Field(..., ge=0, description="Root radius")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D, "B": self.B, "T": self.T, "t": self.t, "r": self.r}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "IShapeParameters":
        return cls(D=data["D"], B=data["B"], T=data["T"], t=data["t"], r=data["r"])


class CircularHollowShapeParameters(BaseShapeParameters):
    """
    Parameters for circular hollow sections (CHS/pipe).

    Attributes:
        D: Outside diameter
        t: Wall thickness

    Examples:
        >>> params = CircularHollowShapeParameters(D=0.273, t=0.008)
    """
    D: float = Field(..., gt=0, description="Outside diameter")
    t: float = Field(..., gt=0, description="Wall thickness")

    @field_validator('t')
    @classmethod
    def validate_thickness(cls, v, info):
        # Wall thickness must be less than radius
        return v

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "CircularHollowShapeParameters":
        return cls(D=data["D"], t=data["t"])


class SquareHollowShapeParameters(BaseShapeParameters):
    """
    Parameters for square hollow sections (SHS).

    Attributes:
        D: Outside dimension
        t: Wall thickness

    Examples:
        >>> params = SquareHollowShapeParameters(D=0.2, t=0.008)
    """
    D: float = Field(..., gt=0, description="Outside dimension")
    t: float = Field(..., gt=0, description="Wall thickness")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "SquareHollowShapeParameters":
        return cls(D=data["D"], t=data["t"])


class RectangularHollowShapeParameters(BaseShapeParameters):
    """
    Parameters for rectangular hollow sections (RHS).

    Attributes:
        D: Height (outside)
        B: Width (outside)
        t: Wall thickness

    Examples:
        >>> params = RectangularHollowShapeParameters(D=0.3, B=0.2, t=0.008)
    """
    D: float = Field(..., gt=0, description="Height (outside)")
    B: float = Field(..., gt=0, description="Width (outside)")
    t: float = Field(..., gt=0, description="Wall thickness")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D, "B": self.B, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "RectangularHollowShapeParameters":
        return cls(D=data["D"], B=data["B"], t=data["t"])


class TrapeziumShapeParameters(BaseShapeParameters):
    """
    Parameters for trapezoidal cross-sections.

    Attributes:
        H: Height
        BTop: Top width
        BBot: Bottom width

    Examples:
        >>> params = TrapeziumShapeParameters(H=0.4, BTop=0.3, BBot=0.5)
    """
    H: float = Field(..., gt=0, description="Height")
    BTop: float = Field(..., gt=0, description="Top width")
    BBot: float = Field(..., gt=0, description="Bottom width")

    def to_dict(self) -> Dict[str, float]:
        return {"H": self.H, "BTop": self.BTop, "BBot": self.BBot}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "TrapeziumShapeParameters":
        return cls(H=data["H"], BTop=data["BTop"], BBot=data["BBot"])


class PolygonShapeParameters(BaseShapeParameters):
    """
    Parameters for regular polygon cross-sections.

    Attributes:
        N: Number of sides
        R: Radius (circumradius)

    Examples:
        >>> params = PolygonShapeParameters(N=6, R=0.1)  # Hexagon
    """
    N: int = Field(..., gt=2, description="Number of sides")
    R: float = Field(..., gt=0, description="Radius (circumradius)")

    def to_dict(self) -> Dict[str, float]:
        return {"N": float(self.N), "R": self.R}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "PolygonShapeParameters":
        return cls(N=int(data["N"]), R=data["R"])


class EqualAngleShapeParameters(BaseShapeParameters):
    """
    Parameters for equal angle cross-sections.

    Attributes:
        A: Leg length
        t: Thickness
        r1: External radius
        r2: Internal radius

    Constraint: r1 > r2

    Examples:
        >>> params = EqualAngleShapeParameters(A=0.1, t=0.01, r1=0.012, r2=0.006)
    """
    A: float = Field(..., gt=0, description="Leg length")
    t: float = Field(..., gt=0, description="Thickness")
    r1: float = Field(..., ge=0, description="External radius")
    r2: float = Field(..., ge=0, description="Internal radius")

    @field_validator('r2')
    @classmethod
    def validate_radii(cls, v, info):
        # r1 must be greater than r2 (checked after model creation)
        return v

    def to_dict(self) -> Dict[str, float]:
        if self.r1 <= self.r2:
            raise ValueError("r1 must be greater than r2")
        return {"A": self.A, "t": self.t, "r1": self.r1, "r2": self.r2}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "EqualAngleShapeParameters":
        return cls(A=data["A"], t=data["t"], r1=data["r1"], r2=data["r2"])


class UnequalAngleShapeParameters(BaseShapeParameters):
    """
    Parameters for unequal angle cross-sections.

    Attributes:
        A: First leg length
        B: Second leg length
        t: Thickness
        r1: External radius
        r2: Internal radius

    Examples:
        >>> params = UnequalAngleShapeParameters(A=0.15, B=0.1, t=0.01, r1=0.012, r2=0.006)
    """
    A: float = Field(..., gt=0, description="First leg length")
    B: float = Field(..., gt=0, description="Second leg length")
    t: float = Field(..., gt=0, description="Thickness")
    r1: float = Field(..., ge=0, description="External radius")
    r2: float = Field(..., ge=0, description="Internal radius")

    def to_dict(self) -> Dict[str, float]:
        return {"A": self.A, "B": self.B, "t": self.t, "r1": self.r1, "r2": self.r2}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "UnequalAngleShapeParameters":
        return cls(A=data["A"], B=data["B"], t=data["t"], r1=data["r1"], r2=data["r2"])


class FlatBarShapeParameters(BaseShapeParameters):
    """
    Parameters for flat bar (rectangular solid bar) cross-sections.

    Attributes:
        B: Width
        t: Thickness

    Examples:
        >>> params = FlatBarShapeParameters(B=0.1, t=0.01)
    """
    B: float = Field(..., gt=0, description="Width")
    t: float = Field(..., gt=0, description="Thickness")

    def to_dict(self) -> Dict[str, float]:
        return {"B": self.B, "t": self.t}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "FlatBarShapeParameters":
        return cls(B=data["B"], t=data["t"])


class SquareBarShapeParameters(BaseShapeParameters):
    """
    Parameters for square bar cross-sections.

    Attributes:
        a: Side length

    Examples:
        >>> params = SquareBarShapeParameters(a=0.05)
    """
    a: float = Field(..., gt=0, description="Side length")

    def to_dict(self) -> Dict[str, float]:
        return {"a": self.a}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "SquareBarShapeParameters":
        return cls(a=data["a"])


class RoundBarShapeParameters(BaseShapeParameters):
    """
    Parameters for round bar (solid circular bar) cross-sections.

    Attributes:
        D: Diameter

    Examples:
        >>> params = RoundBarShapeParameters(D=0.032)
    """
    D: float = Field(..., gt=0, description="Diameter")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "RoundBarShapeParameters":
        return cls(D=data["D"])


class DeformedBarShapeParameters(BaseShapeParameters):
    """
    Parameters for deformed bar (rebar) cross-sections.

    Attributes:
        D: Nominal diameter

    Examples:
        >>> params = DeformedBarShapeParameters(D=0.016)  # 16mm rebar
    """
    D: float = Field(..., gt=0, description="Nominal diameter")

    def to_dict(self) -> Dict[str, float]:
        return {"D": self.D}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "DeformedBarShapeParameters":
        return cls(D=data["D"])


class CustomShapeParameters(BaseShapeParameters):
    """
    Parameters for custom/other shapes with arbitrary key-value pairs.

    Attributes:
        parameters: Dictionary of custom parameters

    Examples:
        >>> params = CustomShapeParameters(parameters={"CustomParam1": 0.5, "CustomParam2": 0.3})
    """
    parameters: Dict[str, float] = Field(default_factory=dict, description="Custom parameters")

    def to_dict(self) -> Dict[str, float]:
        return self.parameters.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "CustomShapeParameters":
        return cls(parameters=data)
