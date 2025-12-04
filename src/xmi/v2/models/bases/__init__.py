"""
Base classes for XMI v2 entities.

This module exports the base classes used for all XMI entities:
- XmiBaseEntity: Root base class for all entities
- XmiBasePhysicalEntity: Base class for physical entities (beams, columns, etc.)
- XmiBaseStructuralAnalyticalEntity: Base class for analytical entities (curve/surface members, etc.)
"""

from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_physical_entity import XmiBasePhysicalEntity
from xmi.v2.models.bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity

__all__ = [
    "XmiBaseEntity",
    "XmiBasePhysicalEntity",
    "XmiBaseStructuralAnalyticalEntity",
]
