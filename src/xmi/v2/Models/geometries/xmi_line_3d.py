from typing import List, Tuple, Optional
from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_point_3d import XmiPoint3D

class XmiLine3D(XmiBaseGeometry):
    start_point: XmiPoint3D = Field(..., alias="StartPoint", description="Start point of the line")
    end_point: XmiPoint3D = Field(..., alias="EndPoint", description="End point of the line")

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
        error_logs: List[Exception] = []

        required_attrs = ("start_point", "end_point")
        missing = [attr for attr in required_attrs if attr not in obj]
        if missing:
            for attr in missing:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
            return None, error_logs

        start_point, start_errors = XmiPoint3D.from_dict(obj["start_point"])
        end_point, end_errors = XmiPoint3D.from_dict(obj["end_point"])
        error_logs.extend(start_errors + end_errors)

        if start_point is None or end_point is None:
            return None, error_logs

        try:
            instance = cls(
                start_point=start_point, 
                end_point=end_point
            )
        except Exception as e:
            error_logs.append(Exception(f"Error instantiating XmiLine3D: {e}"))
            instance = None

        return instance, error_logs
