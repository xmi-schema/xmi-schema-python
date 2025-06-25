from typing import List, Tuple, Optional
from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_point_3d import XmiPoint3D

class XmiLine3D(XmiBaseGeometry):
    start_point: XmiPoint3D = Field(..., description="Start point of the line")
    end_point: XmiPoint3D = Field(..., description="End point of the line")

    @field_validator("start_point", "end_point", mode="before")
    @classmethod
    def check_is_point(cls, v, field):
        if not isinstance(v, XmiPoint3D):
            raise TypeError(f"{field.name} must be an XmiPoint3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def ensure_required_fields(cls, values: dict):
        missing = [field for field in ("start_point", "end_point") if field not in values]
        if missing:
            raise ValueError(f"{', '.join(missing)} are compulsory and must be provided.")
        return values

    @classmethod
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiLine3D"], List[Exception]]:
        errors: List[Exception] = []

        if "start_point" not in obj or "end_point" not in obj:
            if "start_point" not in obj:
                errors.append(Exception("Missing required field: start_point"))
            if "end_point" not in obj:
                errors.append(Exception("Missing required field: end_point"))
            return None, errors

        start_point, start_errors = XmiPoint3D.from_dict(obj["start_point"])
        end_point, end_errors = XmiPoint3D.from_dict(obj["end_point"])
        errors.extend(start_errors + end_errors)

        if start_point is None or end_point is None:
            return None, errors

        try:
            instance = cls(start_point=start_point, end_point=end_point)
        except Exception as e:
            errors.append(e)
            instance = None

        return instance, errors
