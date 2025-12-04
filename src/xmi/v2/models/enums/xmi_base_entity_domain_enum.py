from enum import Enum


class XmiBaseEntityDomainEnum(str, Enum):
    """
    Defines the domain classification for XMI entities.

    This enum categorizes entities into five distinct domains:
    - Physical: Real-world built elements (beams, columns, slabs, walls)
    - StructuralAnalytical: Idealized structural analysis models (curve/surface members, nodes)
    - Geometry: Pure geometric elements (points, lines, arcs)
    - Functional: Functional or operational aspects of the built environment
    - Shared: Cross-domain shared entities (materials, cross-sections)

    The domain type helps organize and filter entities by their primary purpose
    and usage context within the XMI schema.

    Examples:
        >>> from xmi.v2.models.enums.xmi_base_entity_domain_enum import XmiBaseEntityDomainEnum
        >>> domain = XmiBaseEntityDomainEnum.PHYSICAL
        >>> print(domain.value)  # "Physical"
        >>> domain = XmiBaseEntityDomainEnum.STRUCTURAL_ANALYTICAL
        >>> print(domain.value)  # "StructuralAnalytical"

    See Also:
        - XmiBaseEntity: Base class that uses this enum for domain classification
        - XmiBasePhysicalEntity: Sets domain to Physical
        - XmiBaseStructuralAnalyticalEntity: Sets domain to StructuralAnalytical
    """

    PHYSICAL = "Physical"
    STRUCTURAL_ANALYTICAL = "StructuralAnalytical"
    GEOMETRY = "Geometry"
    FUNCTIONAL = "Functional"
    SHARED = "Shared"
