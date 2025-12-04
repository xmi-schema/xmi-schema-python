from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional, Tuple, List, Callable
from ...bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity
from ...geometries.xmi_point_3d import XmiPoint3D
from ..xmi_storey import XmiStorey

class XmiStructuralPointConnection(XmiBaseStructuralAnalyticalEntity):
    point: XmiPoint3D = Field(..., alias="Point")
    storey: Optional[XmiStorey] = Field(None, alias="Storey")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("point")
    @classmethod
    def validate_point(cls, v):
        if not isinstance(v, XmiPoint3D):
            raise TypeError("point should be of type XmiPoint3D")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_entity_type(cls, values):
        values.setdefault("entity_type", "XmiStructuralPointConnection")
        return values
    
    @classmethod
    def from_dict(
        cls,
        obj: dict,
        point_factory: Optional[Callable[[float, float, float], XmiPoint3D]] = None,
    ) -> Tuple[Optional["XmiStructuralPointConnection"], List[Exception]]:
        error_logs = []
        required = ["id", "name", "point"]
        processed = obj.copy()

        def has_key(data: dict, key: str) -> bool:
            variants = {key, key.lower(), key.upper(), key.capitalize()}
            return any(k in data for k in variants)

        for attr in required:
            if not has_key(obj, attr):
                error_logs.append(Exception(f"Missing attribute: {attr}"))
                processed[attr] = None

        point_data = processed.pop("point", None)
        if point_data is None:
            point_data = processed.pop("Point", None)
        if isinstance(point_data, dict):
            def get_coord(key: str):
                value = point_data.get(key)
                return value if value is not None else point_data.get(key.lower())

            x = get_coord("X")
            y = get_coord("Y")
            z = get_coord("Z")
            if point_factory and x is not None and y is not None and z is not None:
                try:
                    processed["point"] = point_factory(float(x), float(y), float(z))
                except Exception as e:
                    error_logs.append(e)
            else:
                point, point_errors = XmiPoint3D.from_dict(point_data)
                processed["point"] = point
                error_logs.extend(point_errors)
        elif isinstance(point_data, XmiPoint3D):
            processed["point"] = point_data
        else:
            error_logs.append(Exception("Point data is missing or invalid"))
            processed["point"] = None

        try:
            instance = cls.model_validate(processed)
        except Exception as e:
            error_logs.append(e)
            instance = None

        return instance, error_logs

    '''@classmethod
    def from_xmi_dict_obj(cls, xmi_dict_obj: dict) -> Tuple[Optional["XmiStructuralPointConnection"], List[Exception]]:
        key_map = {
            "ID": "id",
            "Name": "name",
            "Description": "description",
            "IFCGUID": "ifcguid",
            "Storey": "storey",
        }

        processed = {key_map.get(k, k): v for k, v in xmi_dict_obj.items()}
        return cls.from_dict(processed)'''
