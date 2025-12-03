"""
Unit conversion utilities for XMI schema.

This module provides conversion factors and utilities for converting between
different units of measurement used in structural engineering.
"""

from typing import Dict, Tuple
from ..models.enums.xmi_unit_enum import XmiUnitEnum


# Conversion factors to base SI units (meters for length, m^2 for area, etc.)
CONVERSION_TO_SI_BASE: Dict[XmiUnitEnum, float] = {
    # Length units to meters
    XmiUnitEnum.METER: 1.0,
    XmiUnitEnum.CENTIMETER: 0.01,
    XmiUnitEnum.MILLIMETER: 0.001,
    XmiUnitEnum.INCH: 0.0254,
    XmiUnitEnum.FOOT: 0.3048,
    XmiUnitEnum.YARD: 0.9144,

    # Area units to m^2
    XmiUnitEnum.METER2: 1.0,
    XmiUnitEnum.CENTIMETER2: 0.0001,
    XmiUnitEnum.MILLIMETER2: 0.000001,
    XmiUnitEnum.INCH2: 0.00064516,
    XmiUnitEnum.FOOT2: 0.09290304,

    # Volume units to m^3
    XmiUnitEnum.METER3: 1.0,
    XmiUnitEnum.CENTIMETER3: 0.000001,
    XmiUnitEnum.MILLIMETER3: 0.000000001,
    XmiUnitEnum.INCH3: 0.000016387064,
    XmiUnitEnum.FOOT3: 0.028316846592,

    # Moment of inertia units to m^4
    XmiUnitEnum.METER4: 1.0,
    XmiUnitEnum.CENTIMETER4: 0.00000001,
    XmiUnitEnum.MILLIMETER4: 0.000000000001,
    XmiUnitEnum.INCH4: 0.00000041623143,

    # Time
    XmiUnitEnum.SECOND: 1.0,
}


def convert_value(
    value: float,
    from_unit: XmiUnitEnum,
    to_unit: XmiUnitEnum
) -> float:
    """
    Convert a value from one unit to another.

    Args:
        value: The value to convert
        from_unit: The source unit
        to_unit: The target unit

    Returns:
        float: The converted value

    Raises:
        ValueError: If units are of incompatible types (e.g., length to area)
        KeyError: If unit conversion is not defined

    Examples:
        >>> convert_value(1000.0, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        1.0
        >>> convert_value(1.0, XmiUnitEnum.INCH, XmiUnitEnum.MILLIMETER)
        25.4
        >>> convert_value(100.0, XmiUnitEnum.MILLIMETER2, XmiUnitEnum.CENTIMETER2)
        1.0
    """
    # Quick return if same unit
    if from_unit == to_unit:
        return value

    # Check that units are of the same type
    from_type = XmiUnitEnum.get_base_unit_type(from_unit)
    to_type = XmiUnitEnum.get_base_unit_type(to_unit)

    if from_type != to_type:
        raise ValueError(
            f"Cannot convert between different unit types: "
            f"{from_type} ({from_unit.value}) to {to_type} ({to_unit.value})"
        )

    # Get conversion factors
    if from_unit not in CONVERSION_TO_SI_BASE:
        raise KeyError(f"Conversion factor not defined for unit: {from_unit.value}")
    if to_unit not in CONVERSION_TO_SI_BASE:
        raise KeyError(f"Conversion factor not defined for unit: {to_unit.value}")

    # Convert to SI base, then to target unit
    value_in_si = value * CONVERSION_TO_SI_BASE[from_unit]
    converted_value = value_in_si / CONVERSION_TO_SI_BASE[to_unit]

    return converted_value


def convert_dict(
    values: Dict[str, float],
    from_unit: XmiUnitEnum,
    to_unit: XmiUnitEnum
) -> Dict[str, float]:
    """
    Convert all values in a dictionary from one unit to another.

    Args:
        values: Dictionary of parameter names to values
        from_unit: The source unit
        to_unit: The target unit

    Returns:
        Dict[str, float]: Dictionary with converted values

    Examples:
        >>> params = {"H": 500.0, "B": 300.0}
        >>> convert_dict(params, XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        {"H": 0.5, "B": 0.3}
    """
    return {
        key: convert_value(val, from_unit, to_unit)
        for key, val in values.items()
    }


def get_conversion_factor(
    from_unit: XmiUnitEnum,
    to_unit: XmiUnitEnum
) -> float:
    """
    Get the conversion factor from one unit to another.

    The conversion factor is the number you multiply by to convert from_unit to to_unit.

    Args:
        from_unit: The source unit
        to_unit: The target unit

    Returns:
        float: The conversion factor

    Examples:
        >>> get_conversion_factor(XmiUnitEnum.MILLIMETER, XmiUnitEnum.METER)
        0.001
        >>> get_conversion_factor(XmiUnitEnum.INCH, XmiUnitEnum.MILLIMETER)
        25.4
    """
    # Quick return if same unit
    if from_unit == to_unit:
        return 1.0

    # Check that units are of the same type
    from_type = XmiUnitEnum.get_base_unit_type(from_unit)
    to_type = XmiUnitEnum.get_base_unit_type(to_unit)

    if from_type != to_type:
        raise ValueError(
            f"Cannot get conversion factor between different unit types: "
            f"{from_type} ({from_unit.value}) to {to_type} ({to_unit.value})"
        )

    # Calculate conversion factor
    from_to_si = CONVERSION_TO_SI_BASE[from_unit]
    to_to_si = CONVERSION_TO_SI_BASE[to_unit]

    return from_to_si / to_to_si


def get_common_length_units(metric: bool = True) -> Tuple[XmiUnitEnum, ...]:
    """
    Get commonly used length units for metric or imperial systems.

    Args:
        metric: If True, return metric units; if False, return imperial units

    Returns:
        Tuple of common length units

    Examples:
        >>> get_common_length_units(metric=True)
        (XmiUnitEnum.MILLIMETER, XmiUnitEnum.CENTIMETER, XmiUnitEnum.METER)
        >>> get_common_length_units(metric=False)
        (XmiUnitEnum.INCH, XmiUnitEnum.FOOT)
    """
    if metric:
        return (XmiUnitEnum.MILLIMETER, XmiUnitEnum.CENTIMETER, XmiUnitEnum.METER)
    else:
        return (XmiUnitEnum.INCH, XmiUnitEnum.FOOT, XmiUnitEnum.YARD)


def get_recommended_unit_for_value(
    value: float,
    current_unit: XmiUnitEnum,
    metric: bool = True
) -> XmiUnitEnum:
    """
    Suggest a more appropriate unit for displaying a value.

    This function recommends a unit that would display the value in a
    human-readable range (typically 0.1 to 10000).

    Args:
        value: The numeric value
        current_unit: The current unit of the value
        metric: Whether to recommend metric or imperial units

    Returns:
        XmiUnitEnum: Recommended unit for display

    Examples:
        >>> # 0.001 m is better displayed as 1 mm
        >>> get_recommended_unit_for_value(0.001, XmiUnitEnum.METER)
        XmiUnitEnum.MILLIMETER

        >>> # 2540 mm is better displayed as 2.54 m
        >>> get_recommended_unit_for_value(2540, XmiUnitEnum.MILLIMETER)
        XmiUnitEnum.METER
    """
    unit_type = XmiUnitEnum.get_base_unit_type(current_unit)

    if unit_type == "length":
        common_units = get_common_length_units(metric=metric)
    else:
        # For non-length units, keep the current unit
        return current_unit

    # Try each common unit and find the one that gives the best magnitude
    best_unit = current_unit
    best_score = float('inf')

    for unit in common_units:
        try:
            converted = convert_value(value, current_unit, unit)
            # Score based on how close to the ideal range [1, 1000]
            if 1 <= abs(converted) <= 1000:
                score = 0  # Perfect range
            elif abs(converted) < 1:
                score = 1 / abs(converted)  # Too small
            else:
                score = abs(converted) / 1000  # Too large

            if score < best_score:
                best_score = score
                best_unit = unit
        except (ValueError, KeyError):
            continue

    return best_unit
