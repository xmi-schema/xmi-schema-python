from enum import Enum, unique
from typing import Optional

@unique
class XmiBaseEnum(str, Enum): 
    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return None
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None
    
    @classmethod
    def from_name_get_enum(cls, name_str: str) -> Optional["XmiBaseEnum"]:
        name_str = name_str.upper()
        try:
            return cls[name_str]
        except KeyError:
            return None

    @classmethod
    def from_attribute_get_enum(cls, attribute_str: str) -> "XmiBaseEnum":
        if isinstance(attribute_str, cls):
            return attribute_str

        for member in cls:
            if member.value == attribute_str:
                return member

        raise ValueError(f"Invalid {cls.__name__} value: {attribute_str}")