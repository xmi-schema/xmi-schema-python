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
    

# Testing run python -m src.xmi.v2.models.geometries.xmi_point_3d
    
if __name__ == "__main__":
    print("=== Running Quick Tests for XmiPoint3D ===")

    # Test 1: Valid input
    valid_data = {"x": 1.0, "y": 2.0, "z": 3.0}
    point, errors = XmiPoint3D.from_dict(valid_data)
    print("\n[Valid Input]")
    print("Instance:", point)
    print("Errors:", errors)

    # Test 2: Missing 'z'
    missing_z = {"x": 1.0, "y": 2.0}
    point, errors = XmiPoint3D.from_dict(missing_z)
    print("\n[Missing 'z']")
    print("Instance:", point)
    print("Errors:", [str(e) for e in errors])

    # Test 3: Invalid type for 'x'
    invalid_x = {"x": "a", "y": 2.0, "z": 3.0}
    point, errors = XmiPoint3D.from_dict(invalid_x)
    print("\n[Invalid 'x' Type]")
    print("Instance:", point)
    print("Errors:", [str(e) for e in errors])

    # Test 4: Valid XMI-formatted dict
    xmi_data = {
        "ID": "001",
        "Name": "PointA",
        "X": 10,
        "Y": 20,
        "Z": 30,
        "Description": "Example point"
    }
    point, errors = XmiPoint3D.from_xmi_dict_obj(xmi_data)
    print("\n[XMI-formatted Input]")
    print("Instance:", point.model_dump() if point else None)
    print("Errors:", [str(e) for e in errors])