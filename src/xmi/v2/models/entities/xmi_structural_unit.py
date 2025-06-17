from pydantic import field_validator, model_validator
from typing import Optional, Tuple, List
from uuid import uuid4
from ..enums.xmi_unit_enum import XmiUnitEnum
from ..bases.xmi_base_entity import XmiBaseEntity

class XmiStructuralUnit(XmiBaseEntity):
    Entity: str
    Attribute: str
    Unit: XmiUnitEnum

    @field_validator("Entity")
    @classmethod
    def validate_entity(cls, v):
        if not isinstance(v, str):
            raise TypeError("Entity should be a string.")
        return v

    @field_validator("Attribute")
    @classmethod
    def validate_attribute(cls, v):
        if not isinstance(v, str):
            raise TypeError("Attribute should be a string.")
        return v

    @field_validator("Unit")
    @classmethod
    def validate_unit(cls, v):
        if not isinstance(v, XmiUnitEnum):
            raise TypeError("Unit should be of type XmiUnitEnum")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values):
        if "id" not in values or not values["id"]:
            values["id"] = str(uuid4())
        if "name" not in values or not values["name"]:
            values["name"] = f"{cls.__name__}_{values['id']}"
        values.setdefault("entity_type", "XmiStructuralUnit")
        return values


# Testing run python -m src.xmi.v2.models.entities.xmi_structural_unit
if __name__ == "__main__":
    def test_structural_unit():
        unit = XmiStructuralUnit(
            Entity="XmiBeam",
            Attribute="length",
            Unit=XmiUnitEnum.METER,
            description="Length unit of beam"
        )

        print("Created XmiStructuralUnit:")
        print(unit.model_dump(by_alias=True))

    test_structural_unit()