# Optional, for forward declarations in Python 3.7+
from __future__ import annotations

from ..xmi_base import XmiBaseRelationship, XmiBaseEntity
# from ..entities.xmi_structural_material import XmiStructuralMaterial
# from ..entities.xmi_structural_cross_section import XmiCrossSection
# from ..xmi_errors import XmiInconsistentDataTypeError
from ..constants import *


class XmiHasStructuralMaterial(XmiBaseRelationship):
    __slots__ = XmiBaseRelationship.__slots__

    _attributes_needed = [slot[1:] if slot.startswith(
        '_') else slot for slot in __slots__]

    def __init__(self, source: XmiBaseEntity, target: XmiBaseEntity, name='hasStructuralMaterial', **kwargs):
        name = 'hasStructuralMaterial'
        entity_type = "XmiRelHasSegment"

        # if not isinstance(source, XmiCrossSection):
        #     raise XmiInconsistentDataTypeError(
        #         "'source' parameter needs to be of type XmiCrossSection")
        # if not isinstance(target, XmiStructuralMaterial):
        #     raise XmiInconsistentDataTypeError(
        #         "'target' parameter needs to be of type XmiStructuralMaterial")

        super().__init__(source, target, name, entity_type=entity_type)

        for key, value in kwargs.items():
            if key in self.__slots__:
                # Use the property setter for type checking
                setattr(self, key, value)
