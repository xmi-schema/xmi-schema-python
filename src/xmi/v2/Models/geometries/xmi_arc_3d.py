from typing import Optional, Tuple, List
from pydantic import Field, field_validator, model_validator
from ..bases.xmi_base_geometry import XmiBaseGeometry
from .xmi_point_3d import XmiPoint3D


class XmiArc3D(XmiBaseGeometry):
    start_point: XmiPoint3D = Field(..., description="Start point of the arc")
    end_point: XmiPoint3D = Field(..., description="End point of the arc")
    center_point: XmiPoint3D = Field(..., description="Center point of the arc")
    radius: Optional[float] = Field(None, description="Radius of the arc")

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
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiArc3D"], List[Exception]]:
        error_logs: List[Exception] = []

        missing = [attr for attr in ("start_point", "end_point", "center_point") if attr not in obj]
        if missing:
            for attr in missing:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
            return None, error_logs

        try:
            instance = cls(**obj)
        except Exception as e:
            error_logs.append(Exception(f"Error instantiating XmiArc3D: {e}"))
            instance = None

        return instance, error_logs


# Testing run python -m src.xmi.v2.models.geometries.xmi_arc_3d

if __name__ == "__main__":
    from .xmi_point_3d import XmiPoint3D

    p1 = XmiPoint3D(x=0, y=0, z=0)
    p2 = XmiPoint3D(x=1, y=0, z=0)
    p3 = XmiPoint3D(x=0.5, y=0.5, z=0)

    arc_data = {
        "start_point": p1,
        "end_point": p2,
        "center_point": p3,
        "radius": 0.5,
        "name": "Arc between P1 and P2"
    }

    arc, errors = XmiArc3D.from_dict(arc_data)
    if arc:
        print(arc.model_dump())
    else:
        for e in errors:
            print(f"Error: {e}")