from __future__ import annotations

from typing import Dict, Any, List

from xmi.v2.models.bases.xmi_base_entity import XmiBaseEntity
from xmi.v2.models.bases.xmi_base_relationship import XmiBaseRelationship
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.utils.xmi_entity_type_mapping import ENTITY_TYPE_MAPPING
from xmi.v2.utils.xmi_errors import (
    XmiMissingReferenceInstanceError,
    XmiMissingRequiredAttributeError,
    XmiError
)


class XmiManager:

    def __init__(self):
        self.models: List[XmiModel] = []

    def read_xmi_dict(self, xmi_dict: Dict[str, Any]) -> XmiModel:
        xmi_model = XmiModel()

        for key, entity_list in xmi_dict.items():
            if not isinstance(entity_list, list):
                continue

            for index, item in enumerate(entity_list):
                entity_type = item.get("EntityType")
                entity_class = ENTITY_TYPE_MAPPING.get(entity_type)

                if not entity_type:
                    xmi_model.errors.append(XmiMissingRequiredAttributeError(
                        message="Missing 'EntityType' in item.",
                        problem_data=item
                    ))
                    continue

                if not entity_class:
                    xmi_model.errors.append(XmiMissingReferenceInstanceError(
                        message=f"EntityType '{entity_type}' not found in ENTITY_TYPE_MAPPING.",
                        problem_data=item
                    ))
                    continue

                try:
                    if issubclass(entity_class, XmiBaseEntity):
                        if hasattr(entity_class, 'from_dict'):
                            instance, errors = entity_class.from_dict(item)
                            if instance:
                                xmi_model.entities.append(instance)
                            xmi_model.errors.extend(errors)
                        else:
                            instance = entity_class.model_validate(item)
                            xmi_model.entities.append(instance)
                    elif issubclass(entity_class, XmiBaseRelationship):
                        instance = entity_class.model_validate(item)
                        xmi_model.relationships.append(instance)
                    else:
                        xmi_model.errors.append(XmiError(
                            message=f"Unrecognized entity or relationship type: {entity_type}",
                            problem_data=item
                        ))
                except Exception as e:
                    xmi_model.errors.append(XmiError(
                        message=f"Failed to instantiate '{entity_type}': {str(e)}",
                        problem_data=item
                    ))

        self.models.append(xmi_model)
        return xmi_model
