from __future__ import annotations

from typing import Dict, Any, List
from xmi.v2.models.xmi_model.xmi_model import XmiModel


class XmiManager:

    def __init__(self):
        self.models: List[XmiModel] = []

    def _rearrange_xmi_dict(self, xmi_dict: dict) -> dict:
        desired_order = [
            'StructuralMaterial',
            'StructuralPointConnection',
            'StructuralCrossSection',
            'StructuralCurveMember',
            'StructuralSurfaceMember'
        ]

        rearranged_xmi_dict = {key: xmi_dict[key] for key in desired_order if key in xmi_dict}
        rearranged_xmi_dict.update({key: value for key, value in xmi_dict.items() if key not in desired_order})

        return rearranged_xmi_dict

    def read_xmi_dict(self, xmi_dict: Dict[str, Any]) -> XmiModel:
        rearranged_xmi_dict = self._rearrange_xmi_dict(xmi_dict)

        xmi_model = XmiModel()

        xmi_model.load_from_dict(rearranged_xmi_dict)

        self.models.append(xmi_model)

        return xmi_model