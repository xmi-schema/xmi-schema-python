from pydantic import Field, field_validator, model_validator, ConfigDict
from typing import Optional, Tuple, List
from ..bases.xmi_base_entity import XmiBaseEntity
from ..geometries.xmi_point_3d import XmiPoint3D
from ..entities.xmi_structural_storey import XmiStructuralStorey

class XmiStructuralPointConnection(XmiBaseEntity):
    point: XmiPoint3D = Field(..., alias="Point")
    storey: Optional[XmiStructuralStorey] = Field(None, alias="Storey")

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
    def from_dict(cls, obj: dict) -> Tuple[Optional["XmiStructuralPointConnection"], List[Exception]]:
        error_logs = []
        required = ["id", "name", "point"]
        processed = obj.copy()

        for attr in required:
            if attr not in obj:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
                processed[attr] = None

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
