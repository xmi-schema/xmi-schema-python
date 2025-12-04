from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiUnitEnum(XmiBaseEnum):
    """
    Enumeration of units of measurement for geometric and physical quantities.

    This enum defines both SI (metric) and Imperial units used in the XMI schema
    for dimensions, areas, volumes, and other physical properties.

    Attributes:
        SI Length Units:
            METER: Meter (m) - primary SI length unit
            CENTIMETER: Centimeter (cm) - intermediate length unit
            MILLIMETER: Millimeter (mm) - common for cross-section dimensions

        SI Area Units:
            METER2: Square meter (m²) - area unit for large areas
            MILLIMETER2: Square millimeter (mm²) - cross-section area
            CENTIMETER2: Square centimeter (cm²) - intermediate area

        SI Volume Units:
            METER3: Cubic meter (m³) - volume unit
            MILLIMETER3: Cubic millimeter (mm³) - small volume
            CENTIMETER3: Cubic centimeter (cm³) - intermediate volume

        SI Moment of Inertia Units:
            METER4: Meter to the fourth (m⁴) - moment of inertia (large scale)
            MILLIMETER4: Millimeter to the fourth (mm⁴) - section properties
            CENTIMETER4: Centimeter to the fourth (cm⁴) - intermediate

        Imperial Length Units:
            INCH: Inch (in) - Imperial length unit
            FOOT: Foot (ft) - Imperial length unit
            YARD: Yard (yd) - Imperial length unit

        Imperial Area Units:
            INCH2: Square inch (in²) - Imperial area unit
            FOOT2: Square foot (ft²) - Imperial area unit

        Imperial Volume Units:
            INCH3: Cubic inch (in³) - Imperial volume unit
            FOOT3: Cubic foot (ft³) - Imperial volume unit

        Imperial Moment of Inertia:
            INCH4: Inch to the fourth (in⁴) - Imperial section properties

        Time:
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
        >>> # Imperial units
        >>> unit = XmiUnitEnum.INCH
        >>> print(unit.value)  # "in"
        >>>
        >>> # Use in structural unit
        >>> from xmi.v2.models.entities.xmi_unit import XmiUnit
        >>> length_unit = XmiUnit(
        ...     name="LengthUnit",
        ...     unit=XmiUnitEnum.MILLIMETER
        ... )

    Note:
        Most structural models use either mm system (mm, mm², mm⁴) or m system
        (m, m², m⁴) consistently throughout for proper calculations. Imperial
        units are provided for compatibility with US and UK software exports.
    """
    # SI Length Units
    METER = "m"
    CENTIMETER = "cm"
    MILLIMETER = "mm"

    # SI Area Units
    METER2 = "m^2"
    CENTIMETER2 = "cm^2"
    MILLIMETER2 = "mm^2"

    # SI Volume Units
    METER3 = "m^3"
    CENTIMETER3 = "cm^3"
    MILLIMETER3 = "mm^3"

    # SI Moment of Inertia Units
    METER4 = "m^4"
    CENTIMETER4 = "cm^4"
    MILLIMETER4 = "mm^4"

    # Imperial Length Units
    INCH = "in"
    FOOT = "ft"
    YARD = "yd"

    # Imperial Area Units
    INCH2 = "in^2"
    FOOT2 = "ft^2"

    # Imperial Volume Units
    INCH3 = "in^3"
    FOOT3 = "ft^3"

    # Imperial Moment of Inertia Units
    INCH4 = "in^4"

    # Time
    SECOND = "sec"

    @classmethod
    def get_base_unit_type(cls, unit: "XmiUnitEnum") -> str:
        """
        Get the base unit type (length, area, volume, etc.) for a given unit.

        Args:
            unit: The unit enum value

        Returns:
            str: The base unit type ("length", "area", "volume", "inertia", "time")

        Examples:
            >>> XmiUnitEnum.get_base_unit_type(XmiUnitEnum.MILLIMETER)
            'length'
            >>> XmiUnitEnum.get_base_unit_type(XmiUnitEnum.INCH2)
            'area'
        """
        length_units = {cls.METER, cls.CENTIMETER, cls.MILLIMETER,
                       cls.INCH, cls.FOOT, cls.YARD}
        area_units = {cls.METER2, cls.CENTIMETER2, cls.MILLIMETER2,
                     cls.INCH2, cls.FOOT2}
        volume_units = {cls.METER3, cls.CENTIMETER3, cls.MILLIMETER3,
                       cls.INCH3, cls.FOOT3}
        inertia_units = {cls.METER4, cls.CENTIMETER4, cls.MILLIMETER4, cls.INCH4}

        if unit in length_units:
            return "length"
        elif unit in area_units:
            return "area"
        elif unit in volume_units:
            return "volume"
        elif unit in inertia_units:
            return "inertia"
        elif unit == cls.SECOND:
            return "time"
        else:
            return "unknown"

    @classmethod
    def is_metric(cls, unit: "XmiUnitEnum") -> bool:
        """
        Check if a unit is metric (SI).

        Args:
            unit: The unit enum value

        Returns:
            bool: True if metric, False if imperial

        Examples:
            >>> XmiUnitEnum.is_metric(XmiUnitEnum.MILLIMETER)
            True
            >>> XmiUnitEnum.is_metric(XmiUnitEnum.INCH)
            False
        """
        metric_units = {
            cls.METER, cls.CENTIMETER, cls.MILLIMETER,
            cls.METER2, cls.CENTIMETER2, cls.MILLIMETER2,
            cls.METER3, cls.CENTIMETER3, cls.MILLIMETER3,
            cls.METER4, cls.CENTIMETER4, cls.MILLIMETER4,
            cls.SECOND
        }
        return unit in metric_units
