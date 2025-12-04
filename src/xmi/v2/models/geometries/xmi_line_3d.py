from typing import List, Tuple, Optional, Callable
from pydantic import Field, field_validator, model_validator, ValidationInfo
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_point_3d import XmiPoint3D

class XmiLine3D(XmiBaseGeometry):
    start_point: XmiPoint3D = Field(..., alias="StartPoint", description="Start point of the line")
    end_point: XmiPoint3D = Field(..., alias="EndPoint", description="End point of the line")

    @field_validator("start_point", "end_point", mode="before")
    @classmethod
    def check_is_point(cls, v, info: ValidationInfo):
        if not isinstance(v, XmiPoint3D):
            raise TypeError(f"{info.field_name} must be an XmiPoint3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def ensure_required_fields(cls, values: dict):
        missing = [field for field in ("start_point", "end_point") if field not in values]
        if missing:
            raise ValueError(f"{', '.join(missing)} are compulsory and must be provided.")
        return values

    @classmethod
    def from_dict(
        cls,
        obj: dict,
        point_factory: Optional[Callable[[float, float, float], XmiPoint3D]] = None,
    ) -> Tuple[Optional["XmiLine3D"], List[Exception]]:
        error_logs: List[Exception] = []

        def get_section(key: str):
            candidates = [
                key,
                key.lower(),
                key.upper(),
                key.title().replace("_", ""),
            ]
            for candidate in candidates:
                if candidate in obj:
                    return obj[candidate]
            return None

        required_attrs = ("start_point", "end_point")
        missing = [attr for attr in required_attrs if get_section(attr) is None]
        if missing:
            for attr in missing:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
            return None, error_logs

        def make_point(data: dict) -> Tuple[Optional[XmiPoint3D], List[Exception]]:
            if not isinstance(data, dict):
                return None, [Exception("Point data must be a dict")]
            if point_factory:
                try:
                    def coord(key: str):
                        value = data.get(key)
                        return value if value is not None else data.get(key.lower())

                    x = float(coord("X"))
                    y = float(coord("Y"))
                    z = float(coord("Z"))
                except (TypeError, ValueError) as exc:
                    return None, [Exception(f"Invalid point data: {exc}")]
                try:
                    return point_factory(x, y, z), []
                except Exception as exc:
                    return None, [exc]
            return XmiPoint3D.from_dict(data)

        start_point, start_errors = make_point(get_section("start_point"))
        end_point, end_errors = make_point(get_section("end_point"))
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
