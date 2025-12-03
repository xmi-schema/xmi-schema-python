from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiUnitEnum(XmiBaseEnum):
    """
    Enumeration of units of measurement for geometric and physical quantities.

    This enum defines the SI (metric) units used in the XMI schema for dimensions,
    areas, volumes, and other physical properties.

    Attributes:
        METER: Meter (m) - primary length unit
        CENTIMETER: Centimeter (cm) - intermediate length unit
        MILLIMETER: Millimeter (mm) - common for cross-section dimensions
        METER2: Square meter (m²) - area unit for large areas
        MILLIMETER2: Square millimeter (mm²) - cross-section area
        METER3: Cubic meter (m³) - volume unit
        MILLIMETER3: Cubic millimeter (mm³) - small volume
        METER4: Meter to the fourth (m⁴) - moment of inertia (large scale)
        MILLIMETER4: Millimeter to the fourth (mm⁴) - section properties
        SECOND: Second (sec) - time unit

    Examples:
        >>> from xmi.v2.models.enums.xmi_unit_enum import XmiUnitEnum
        >>> # Direct access
        >>> unit = XmiUnitEnum.MILLIMETER
        >>> print(unit.value)  # "mm"
        >>>
        >>> # Case-insensitive lookup
        >>> unit = XmiUnitEnum("m^2")  # Returns METER2
        >>>
        >>> # Use in structural unit
        >>> from xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit
        >>> length_unit = XmiStructuralUnit(
        ...     name="LengthUnit",
        ...     unit=XmiUnitEnum.MILLIMETER
        ... )

    Note:
        Most structural models use either mm system (mm, mm², mm⁴) or m system
        (m, m², m⁴) consistently throughout for proper calculations.
    """
    METER3 = "m^3"
    METER2 = "m^2"
    METER = "m"
    METER4 = "m^4"
    MILLIMETER4 = "mm^4"
    MILLIMETER = "mm"
    CENTIMETER = "cm"
    MILLIMETER3 = "mm^3"
    MILLIMETER2 = "mm^2"
    SECOND = "sec"
