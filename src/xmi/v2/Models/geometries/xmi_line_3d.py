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

        missing = [attr for attr in ("start_point", "end_point") if attr not in obj]
        if missing:
            for attr in missing:
                errors.append(Exception(f"Missing required field: {attr}"))
            return None, errors

        try:
            instance = cls(**obj)
        except Exception as e:
            errors.append(e)
            instance = None

        return instance, errors


# Testing run python -m src.xmi.v2.models.geometries.xmi_line_3d

if __name__ == "__main__":
    point1 = XmiPoint3D(x=0.0, y=0.0, z=0.0, name="Start", id="p1")
    point2 = XmiPoint3D(x=10.0, y=5.0, z=2.0, name="End", id="p2")

    line_data = {
        "start_point": point1,
        "end_point": point2,
        "name": "TestLine",
        "id": "line123",
        "description": "A simple test line"
    }

    line_instance, errors = XmiLine3D.from_dict(line_data)

    if errors:
        print("Errors during instantiation:")
        for e in errors:
            print(" -", e)
    else:
        print("Line created successfully:")
        print(line_instance.model_dump(by_alias=True))