from enum import Enum, unique
from typing import Optional
from pydantic import BaseModel, field_validator

@unique
class XmiBaseEnum(str, Enum): 
    @classmethod
    def from_name_get_enum(cls, name_str: str) -> Optional["XmiBaseEnum"]:
        name_str = name_str.upper()
        try:
            return cls[name_str]
        except KeyError:
            return None

    @classmethod
    def from_attribute_get_enum(cls, attribute_str: str) -> Optional["XmiBaseEnum"]:
        for member in cls:
            if member.value == attribute_str:
                return member
        return None