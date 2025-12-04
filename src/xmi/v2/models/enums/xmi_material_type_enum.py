from enum import unique

from ..bases.xmi_base_enum import XmiBaseEnum


@unique
class XmiMaterialTypeEnum(XmiBaseEnum):
    """
    Enumeration of structural material types supported by the XMI schema.

    The enum mirrors the legacy v1 set to maintain compatibility with the C#
    reference implementation. Material type drives entity validation as well
    as downstream calculations such as unit weights or modulus assignments.
    """

    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINIUM = "Aluminium"
    COMPOSITE = "Composite"
    MASONRY = "Masonry"
    OTHERS = "Others"
    REBAR = "Rebar"  # Marked for future removal
    TENDON = "Tendon"  # Marked for future removal


