from enum import Enum, unique
from typing import Optional

@unique
class XmiBaseEnum(str, Enum):
    """
    Base class for all enumeration types in the XMI schema v2 implementation.

    This class provides case-insensitive enum lookup, flexible enum creation from
    names or attribute values, and robust error handling for invalid enum values.
    It extends Python's Enum to support the XMI schema's string-based enumeration
    patterns.

    Key Features:
        - Case-insensitive lookup via _missing_() method
        - String-based enum (inherits from both str and Enum)
        - Unique values enforced by @unique decorator
        - Multiple lookup methods: by name, by value, by case-insensitive value
        - Seamless integration with Pydantic validation

    Examples:
        >>> from xmi.v2.models.bases.xmi_base_enum import XmiBaseEnum
        >>> from enum import unique
        >>>
        >>> @unique
        ... class MaterialType(XmiBaseEnum):
        ...     CONCRETE = "Concrete"
        ...     STEEL = "Steel"
        ...     TIMBER = "Timber"
        >>>
        >>> # Method 1: Direct access
        >>> mat1 = MaterialType.CONCRETE
        >>> print(mat1.value)  # "Concrete"
        >>>
        >>> # Method 2: Case-insensitive lookup (via _missing_)
        >>> mat2 = MaterialType("concrete")  # Returns MaterialType.CONCRETE
        >>> mat3 = MaterialType("CONCRETE")  # Returns MaterialType.CONCRETE
        >>>
        >>> # Method 3: From name
        >>> mat4 = MaterialType.from_name_get_enum("concrete")  # MaterialType.CONCRETE
        >>>
        >>> # Method 4: From attribute (exact value match)
        >>> mat5 = MaterialType.from_attribute_get_enum("Concrete")  # MaterialType.CONCRETE

    Note:
        Subclasses should use the @unique decorator to ensure no duplicate values.
        All enum values should be strings to maintain compatibility with the XMI schema.
    """ 
    @classmethod
    def _missing_(cls, value):
        """
        Provides case-insensitive enum lookup fallback.

        This method is automatically called by Python's Enum when standard lookup fails.
        It performs a case-insensitive comparison of the value against all enum members.

        Args:
            value: The value to look up (should be a string)

        Returns:
            Enum member if found (case-insensitive match), None otherwise

        Examples:
            >>> class MaterialType(XmiBaseEnum):
            ...     CONCRETE = "Concrete"
            ...     STEEL = "Steel"
            >>>
            >>> # All of these work via _missing_:
            >>> MaterialType("concrete")  # Returns MaterialType.CONCRETE
            >>> MaterialType("CONCRETE")  # Returns MaterialType.CONCRETE
            >>> MaterialType("Concrete")  # Returns MaterialType.CONCRETE (exact match first)
            >>> MaterialType(123)  # Returns None (not a string)
        """
        if not isinstance(value, str):
            return None
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None
    
    @classmethod
    def from_name_get_enum(cls, name_str: str) -> Optional["XmiBaseEnum"]:
        """
        Get enum member by its name (e.g., "CONCRETE", "STEEL").

        This method looks up an enum member by its member name (not value).
        The input is converted to uppercase before lookup.

        Args:
            name_str: The enum member name to look up (case-insensitive)

        Returns:
            Enum member if found, None if not found

        Examples:
            >>> class MaterialType(XmiBaseEnum):
            ...     CONCRETE = "Concrete"
            ...     STEEL = "Steel"
            >>>
            >>> # Lookup by name (all case variations work)
            >>> MaterialType.from_name_get_enum("concrete")  # MaterialType.CONCRETE
            >>> MaterialType.from_name_get_enum("CONCRETE")  # MaterialType.CONCRETE
            >>> MaterialType.from_name_get_enum("steel")     # MaterialType.STEEL
            >>> MaterialType.from_name_get_enum("invalid")   # None
        """
        name_str = name_str.upper()
        try:
            return cls[name_str]
        except KeyError:
            return None

    @classmethod
    def from_attribute_get_enum(cls, attribute_str: str) -> "XmiBaseEnum":
        """
        Get enum member by its value (e.g., "Concrete", "Steel").

        This method looks up an enum member by its attribute value (not name).
        Unlike _missing_(), this method is case-sensitive and performs exact matching.
        If the input is already an enum instance, it returns it unchanged.

        Args:
            attribute_str: The enum value to look up, or an existing enum instance

        Returns:
            Enum member matching the value

        Raises:
            ValueError: If the value is not found in the enum

        Examples:
            >>> class MaterialType(XmiBaseEnum):
            ...     CONCRETE = "Concrete"
            ...     STEEL = "Steel"
            >>>
            >>> # Lookup by value (case-sensitive!)
            >>> MaterialType.from_attribute_get_enum("Concrete")  # MaterialType.CONCRETE
            >>> MaterialType.from_attribute_get_enum("Steel")     # MaterialType.STEEL
            >>>
            >>> # Pass-through if already enum
            >>> mat = MaterialType.CONCRETE
            >>> MaterialType.from_attribute_get_enum(mat)  # Returns mat unchanged
            >>>
            >>> # Raises ValueError (case-sensitive)
            >>> MaterialType.from_attribute_get_enum("concrete")  # ValueError!
            >>> MaterialType.from_attribute_get_enum("Invalid")   # ValueError!
        """
        if isinstance(attribute_str, cls):
            return attribute_str

        for member in cls:
            if member.value == attribute_str:
                return member

        raise ValueError(f"Invalid {cls.__name__} value: {attribute_str}")