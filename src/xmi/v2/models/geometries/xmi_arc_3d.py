from typing import Optional, Tuple, List, Callable
from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_point_3d import XmiPoint3D


class XmiArc3D(XmiBaseGeometry):
    start_point: XmiPoint3D = Field(..., alias="StartPoint", description="Start point of the arc")
    end_point: XmiPoint3D = Field(..., alias="EndPoint", description="End point of the arc")
    center_point: XmiPoint3D = Field(..., alias="CenterPoint", description="Center point of the arc")
    radius: Optional[float] = Field(None, alias="Radius", description="Radius of the arc")

    @field_validator("start_point", "end_point", "center_point", mode="before")
    @classmethod
    def validate_points(cls, v, field):
        if not isinstance(v, XmiPoint3D):
            raise TypeError(f"{field.name} should be an XmiPoint3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def ensure_required_fields(cls, values):
        missing = [attr for attr in ("start_point", "end_point", "center_point") if attr not in values]
        if missing:
            raise ValueError(f"{', '.join(missing)} are compulsory and must be provided.")
        return values

    @classmethod
    def from_dict(
        cls,
        obj: dict,
        point_factory: Optional[Callable[[float, float, float], XmiPoint3D]] = None,
    ) -> Tuple[Optional["XmiArc3D"], List[Exception]]:
        error_logs: List[Exception] = []
        processed = obj.copy()

        def get_section(key: str):
            candidates = [
                key,
                key.lower(),
                key.upper(),
                key.title().replace("_", ""),
            ]
            for candidate in candidates:
                if candidate in processed:
                    return processed[candidate]
            return None

        required_attrs = ("start_point", "end_point", "center_point")
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
        center_point, center_errors = make_point(get_section("center_point"))
        error_logs.extend(start_errors + end_errors + center_errors)

        if start_point is None or end_point is None or center_point is None:
            return None, error_logs

        try:
            instance = cls(
                start_point=start_point,
                end_point=end_point,
                center_point=center_point,
                radius=obj.get("radius"),
                name=obj.get("name")
            )
        except Exception as e:
            error_logs.append(Exception(f"Error instantiating XmiArc3D: {e}"))
            instance = None

        return instance, error_logs
