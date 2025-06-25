from pydantic import Field, field_validator
from typing import Tuple, List, Optional
from ..bases.xmi_base_geometry import XmiBaseGeometry

class XmiPoint3D(XmiBaseGeometry):
    x: float = Field(..., alias="X", description="X coordinate")
    y: float = Field(..., alias="Y", description="Y coordinate")
    z: float = Field(..., alias="Z", description="Z coordinate")

    @field_validator("x", "y", "z")
    @classmethod
    def check_coordinate(cls, v, field):
        if not isinstance(v, (int, float)):
            raise TypeError(f"{field.name} must be a number")
        return float(v)

    @classmethod
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiPoint3D"], List[Exception]]:
        error_logs: List[Exception] = []
        processed_data = obj.copy()

        required_attrs = ["X", "Y", "Z"]
        for attr in required_attrs:
            if attr not in processed_data:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
                processed_data[attr] = None

        try:
            instance = cls.model_validate(processed_data)
        except Exception as e:
            error_logs.append(e)
            instance = None

        return instance, error_logs

    @classmethod
    def from_xmi_dict_obj(cls, xmi_dict_obj: dict) -> Tuple["XmiPoint3D", List[Exception]]:
        key_map = {
            "Name": "name",
            "X": "x",
            "Y": "y",
            "Z": "z",
            "Description": "description",
            "ID": "id",
            "IFCGUID": "ifcguid",
        }

        processed = {key_map.get(k, k): v for k, v in xmi_dict_obj.items()}
        return cls.from_dict(processed)
    