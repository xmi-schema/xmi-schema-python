from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiShapeEnum(XmiBaseEnum):
    """
    Enumeration of cross-sectional shapes for structural members.

    This enum defines the geometric profile shapes available for structural
    cross-sections. The shape determines the section's geometric properties,
    material distribution, and structural behavior.

    Attributes:
        RECTANGULAR: Solid rectangular cross-section (concrete beams, columns)
        CIRCULAR: Solid circular cross-section (concrete columns, piles)
        L_SHAPE: L-shaped angle cross-section (steel angles)
        T_SHAPE: T-shaped cross-section (steel T-sections)
        C_SHAPE: C-shaped channel cross-section (steel channels)
        I_SHAPE: I-shaped wide flange cross-section (steel I-beams)
        SQUARE_HOLLOW: Hollow square cross-section (steel hollow sections)
        RECTANGULAR_HOLLOW: Hollow rectangular cross-section (steel hollow sections)
        OTHERS: Custom or non-standard shapes
        UNKNOWN: Shape not specified or unknown

    Examples:
        >>> from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
        >>> # Direct access
        >>> shape = XmiShapeEnum.RECTANGULAR
        >>> print(shape.value)  # "Rectangular"
        >>>
        >>> # Case-insensitive lookup
        >>> shape = XmiShapeEnum("i shape")  # Returns I_SHAPE
        >>>
        >>> # Use in cross-section
        >>> from xmi.v2.models.entities.xmi_structural_cross_section import XmiCrossSection
        >>> section = XmiCrossSection(
        ...     name="RECT_300x500",
        ...     shape=XmiShapeEnum.RECTANGULAR,
        ...     width=300,
        ...     height=500
        ... )

    Note:
        Different shapes require different dimensional parameters. For example,
        RECTANGULAR requires width and height, while CIRCULAR requires diameter.
    """
    RECTANGULAR = "Rectangular"
    CIRCULAR = "Circular"
    L_SHAPE = "L Shape"
    T_SHAPE = "T Shape"
    C_SHAPE = "C Shape"
    I_SHAPE = "I Shape"
    SQUARE_HOLLOW = "Square Hollow"
    RECTANGULAR_HOLLOW = "Rectangular Hollow"
    OTHERS = "Others"
    UNKNOWN = "Unknown"