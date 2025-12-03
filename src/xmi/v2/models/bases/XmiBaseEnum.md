# XmiBaseEnum

## Overview

`XmiBaseEnum` is the base class for all enumeration types in the XMI schema v2 implementation. It provides case-insensitive enum lookup, flexible enum creation from names or attribute values, and robust error handling for invalid enum values. This base class extends Python's `Enum` to support the XMI schema's string-based enumeration patterns.

## Class Hierarchy

- **Parent**: `str`, `Enum`
- **Decorator**: `@unique` (ensures no duplicate values)
- **Version**: v2 (Pydantic-based implementation)
- **Module**: `src/xmi/v2/models/bases/xmi_base_enum.py`
- **Children**: All XMI enum classes (MaterialType, SegmentType, CrossSectionShape, etc.)

## Purpose and Functionality

### Key Features

1. **Case-Insensitive Lookup**: Automatically handles uppercase, lowercase, or mixed case
2. **Flexible Creation**: Create enum from name or attribute value
3. **String-Based**: Inherits from `str` for easy serialization and comparison
4. **Unique Values**: `@unique` decorator prevents duplicate enum values
5. **Missing Value Handler**: Custom `_missing_()` method for case-insensitive fallback

### Enum Lookup Methods

#### 1. Standard Enum Access
```python
# Normal Python enum access (case-sensitive)
value = MyEnum.OPTION_ONE
```

#### 2. Case-Insensitive Lookup via `_missing_`
```python
# Automatically called when standard lookup fails
# Tries lowercase comparison
value = MyEnum("option_one")  # Finds OPTION_ONE
value = MyEnum("Option_One")  # Finds OPTION_ONE
```

#### 3. From Name (`from_name_get_enum`)
```python
# Lookup by enum member name (converted to uppercase)
value = MyEnum.from_name_get_enum("option_one")  # Returns MyEnum.OPTION_ONE or None
```

#### 4. From Attribute (`from_attribute_get_enum`)
```python
# Lookup by enum value (exact match)
value = MyEnum.from_attribute_get_enum("concrete")  # Returns member with value "concrete"
```

## Methods

### `_missing_(cls, value)`

**Purpose**: Provides case-insensitive enum lookup fallback

**Parameters:**
- `value`: The value to look up (should be string)

**Returns:**
- Enum member if found (case-insensitive match)
- `None` if not found or value is not a string

**Behavior:**
```python
class MaterialType(XmiBaseEnum):
    CONCRETE = "Concrete"
    STEEL = "Steel"

# All of these work via _missing_:
MaterialType("concrete")  # Returns MaterialType.CONCRETE
MaterialType("CONCRETE")  # Returns MaterialType.CONCRETE
MaterialType("Concrete")  # Returns MaterialType.CONCRETE (exact match)
MaterialType(123)         # Returns None (not a string)
```

### `from_name_get_enum(cls, name_str: str) -> Optional["XmiBaseEnum"]`

**Purpose**: Get enum member by its name (e.g., "CONCRETE", "STEEL")

**Parameters:**
- `name_str`: The enum member name to look up

**Returns:**
- Enum member if found
- `None` if not found

**Behavior:**
- Converts input to uppercase
- Performs exact name match
- Returns `None` on `KeyError` (not found)

**Example:**
```python
class MaterialType(XmiBaseEnum):
    CONCRETE = "Concrete"
    STEEL = "Steel"

# Lookup by name
MaterialType.from_name_get_enum("concrete")  # MaterialType.CONCRETE
MaterialType.from_name_get_enum("CONCRETE")  # MaterialType.CONCRETE
MaterialType.from_name_get_enum("steel")     # MaterialType.STEEL
MaterialType.from_name_get_enum("invalid")   # None
```

### `from_attribute_get_enum(cls, attribute_str: str) -> "XmiBaseEnum"`

**Purpose**: Get enum member by its value (e.g., "Concrete", "Steel")

**Parameters:**
- `attribute_str`: The enum value to look up, or an existing enum instance

**Returns:**
- Enum member if found
- Raises `ValueError` if not found

**Behavior:**
- If input is already an enum instance, return it unchanged
- Otherwise, search for member with matching value
- Raises `ValueError` with descriptive message if not found
- **Case-sensitive** exact match on value

**Example:**
```python
class MaterialType(XmiBaseEnum):
    CONCRETE = "Concrete"
    STEEL = "Steel"

# Lookup by value
MaterialType.from_attribute_get_enum("Concrete")  # MaterialType.CONCRETE
MaterialType.from_attribute_get_enum("Steel")     # MaterialType.STEEL

# Pass-through if already enum
mat = MaterialType.CONCRETE
MaterialType.from_attribute_get_enum(mat)  # Returns mat unchanged

# Raises ValueError
MaterialType.from_attribute_get_enum("concrete")  # ValueError: Invalid MaterialType value: concrete
MaterialType.from_attribute_get_enum("Invalid")   # ValueError: Invalid MaterialType value: Invalid
```

## Usage Examples

### Defining Custom Enums

```python
from xmi.v2.models.bases.xmi_base_enum import XmiBaseEnum
from enum import unique

@unique
class MaterialType(XmiBaseEnum):
    """Enumeration of structural material types."""
    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINUM = "Aluminum"
    MASONRY = "Masonry"

@unique
class SegmentType(XmiBaseEnum):
    """Enumeration of geometric segment types."""
    LINE = "Line"
    CIRCULAR_ARC = "CircularArc"
    PARABOLIC_ARC = "ParabolicArc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
```

### Creating Enum Instances

```python
# Method 1: Direct access (standard Python enum)
mat1 = MaterialType.CONCRETE
print(mat1)  # MaterialType.CONCRETE
print(mat1.value)  # "Concrete"

# Method 2: Case-insensitive value lookup (via _missing_)
mat2 = MaterialType("concrete")
mat3 = MaterialType("CONCRETE")
mat4 = MaterialType("Concrete")
# All return MaterialType.CONCRETE

# Method 3: From name (member name lookup)
mat5 = MaterialType.from_name_get_enum("concrete")
mat6 = MaterialType.from_name_get_enum("STEEL")

# Method 4: From attribute (value lookup)
mat7 = MaterialType.from_attribute_get_enum("Concrete")
mat8 = MaterialType.from_attribute_get_enum("Steel")
```

### Common Patterns

#### Parsing XMI String Values

```python
def parse_material_type(type_str: str) -> Optional[MaterialType]:
    """Parse material type from XMI string (case-insensitive)."""
    try:
        return MaterialType(type_str)
    except (ValueError, KeyError):
        return None

# Usage
mat = parse_material_type("concrete")  # MaterialType.CONCRETE
mat = parse_material_type("STEEL")     # MaterialType.STEEL
mat = parse_material_type("invalid")   # None
```

#### Validating Enum Values

```python
def validate_material_type(type_str: str) -> bool:
    """Check if a string is a valid material type."""
    try:
        MaterialType.from_attribute_get_enum(type_str)
        return True
    except ValueError:
        return False

# Usage
is_valid = validate_material_type("Concrete")  # True
is_valid = validate_material_type("concrete")  # False (case-sensitive!)
is_valid = validate_material_type("Invalid")   # False
```

#### Safe Enum Conversion

```python
def get_material_or_default(type_str: str, default=MaterialType.CONCRETE):
    """Get material type with fallback to default."""
    # Try case-insensitive lookup
    mat = MaterialType(type_str) if isinstance(type_str, str) else None
    return mat if mat else default

# Usage
mat1 = get_material_or_default("steel")    # MaterialType.STEEL
mat2 = get_material_or_default("invalid")  # MaterialType.CONCRETE (default)
mat3 = get_material_or_default(None)       # MaterialType.CONCRETE (default)
```

#### Getting All Enum Values

```python
def get_all_material_types():
    """Get list of all material type values."""
    return [member.value for member in MaterialType]

def get_all_material_names():
    """Get list of all material type member names."""
    return [member.name for member in MaterialType]

# Usage
values = get_all_material_types()
# ["Concrete", "Steel", "Timber", "Aluminum", "Masonry"]

names = get_all_material_names()
# ["CONCRETE", "STEEL", "TIMBER", "ALUMINUM", "MASONRY"]
```

#### Enum to String Conversion

```python
def material_to_string(material: MaterialType) -> str:
    """Convert material enum to string value."""
    return material.value

# Usage
mat = MaterialType.CONCRETE
string_value = material_to_string(mat)  # "Concrete"

# Or directly:
string_value = mat.value  # "Concrete"
```

#### String Comparison

```python
# Since XmiBaseEnum inherits from str, direct comparison works:
mat = MaterialType.CONCRETE

# These all work:
if mat == "Concrete":
    print("Is concrete")

if mat.value == "Concrete":
    print("Is concrete")

if str(mat) == "MaterialType.CONCRETE":
    print("String representation match")
```

#### Creating Enum from User Input

```python
def create_material_from_input(user_input: str):
    """Create material type from user input with validation."""
    # Clean input
    cleaned = user_input.strip()

    # Try case-insensitive lookup
    try:
        material = MaterialType(cleaned.lower())
        return material, None
    except (ValueError, KeyError):
        pass

    # Try name lookup
    material = MaterialType.from_name_get_enum(cleaned)
    if material:
        return material, None

    # Try attribute lookup
    try:
        material = MaterialType.from_attribute_get_enum(cleaned)
        return material, None
    except ValueError:
        pass

    # Failed to create
    valid_values = [m.value for m in MaterialType]
    return None, f"Invalid material type. Valid options: {', '.join(valid_values)}"

# Usage
mat, error = create_material_from_input("concrete")
# (MaterialType.CONCRETE, None)

mat, error = create_material_from_input("Concrete")
# (MaterialType.CONCRETE, None)

mat, error = create_material_from_input("invalid")
# (None, "Invalid material type. Valid options: Concrete, Steel, Timber, Aluminum, Masonry")
```

#### Enum Mapping Dictionaries

```python
# Create mapping from enum to properties
MATERIAL_PROPERTIES = {
    MaterialType.CONCRETE: {"density": 2400, "color": "grey"},
    MaterialType.STEEL: {"density": 7850, "color": "silver"},
    MaterialType.TIMBER: {"density": 600, "color": "brown"},
}

def get_material_density(material: MaterialType) -> float:
    """Get density for a material type."""
    return MATERIAL_PROPERTIES.get(material, {}).get("density", 0)

# Usage
density = get_material_density(MaterialType.CONCRETE)  # 2400
```

#### Iterating Over Enums

```python
def print_all_materials():
    """Print all available material types."""
    print("Available material types:")
    for material in MaterialType:
        print(f"  - {material.name}: {material.value}")

# Output:
# Available material types:
#   - CONCRETE: Concrete
#   - STEEL: Steel
#   - TIMBER: Timber
#   - ALUMINUM: Aluminum
#   - MASONRY: Masonry
```

## Integration with Pydantic Models

### Using Enums in Pydantic Fields

```python
from pydantic import BaseModel, Field
from typing import Optional

class XmiStructuralMaterial(BaseModel):
    """Structural material entity with enum validation."""
    name: str
    material_type: MaterialType = Field(..., alias="MaterialType")
    grade: Optional[str] = None

    class Config:
        use_enum_values = True  # Serialize enum as value, not name

# Create instance
material = XmiStructuralMaterial(
    name="C30",
    material_type=MaterialType.CONCRETE,
    grade="C30/37"
)

# From dictionary (Pydantic handles enum conversion)
material_dict = {
    "name": "C30",
    "MaterialType": "Concrete",  # String is converted to enum
    "grade": "C30/37"
}
material = XmiStructuralMaterial.model_validate(material_dict)
print(material.material_type)  # MaterialType.CONCRETE
```

### Enum Validation in Pydantic

```python
from pydantic import field_validator

class XmiStructuralMaterial(BaseModel):
    material_type: MaterialType

    @field_validator('material_type', mode='before')
    @classmethod
    def validate_material_type(cls, v):
        """Custom validator for flexible material type input."""
        if isinstance(v, MaterialType):
            return v

        if isinstance(v, str):
            # Try case-insensitive lookup
            try:
                return MaterialType(v.lower())
            except (ValueError, KeyError):
                pass

            # Try exact value lookup
            try:
                return MaterialType.from_attribute_get_enum(v)
            except ValueError:
                raise ValueError(f"Invalid material type: {v}")

        raise ValueError(f"Material type must be string or MaterialType enum, got {type(v)}")
```

## Validation Rules

### Uniqueness

The `@unique` decorator ensures:
- No two enum members can have the same value
- Raises `ValueError` if duplicate values are defined

```python
# This will raise ValueError:
@unique
class BadEnum(XmiBaseEnum):
    OPTION1 = "value"
    OPTION2 = "value"  # Error! Duplicate value
```

### String Inheritance

All enum members are strings:
```python
mat = MaterialType.CONCRETE
isinstance(mat, str)  # True
isinstance(mat, MaterialType)  # True
```

### Case Sensitivity

- `_missing_()`: Case-insensitive (converts to lowercase)
- `from_name_get_enum()`: Case-insensitive (converts to uppercase)
- `from_attribute_get_enum()`: **Case-sensitive** exact match

## Notes

### Version Differences (v1 vs v2)

**v2 Characteristics (XmiBaseEnum):**
- Inherits from `str` and `Enum`
- Case-insensitive lookup via `_missing_()`
- Multiple lookup methods for flexibility
- Works seamlessly with Pydantic validation
- `@unique` decorator prevents duplicates

**v1 Characteristics:**
- May use simple string constants or different enum implementation
- Less flexible enum handling
- Manual validation required

### Why Inherit from `str`?

Inheriting from both `str` and `Enum` provides:
1. **Serialization**: Enums serialize naturally as strings
2. **Comparison**: Can compare directly with strings
3. **Type Hinting**: Works as both string and enum type
4. **JSON Compatibility**: Automatically JSON-serializable

### Performance Considerations

- Enum lookup is O(n) where n = number of enum members
- Typically small n (< 20 members per enum)
- Case-insensitive lookup adds minimal overhead
- Enum instances are singletons (memory efficient)

### Common Pitfalls

1. **Case Sensitivity in `from_attribute_get_enum`**: This method is case-sensitive
   ```python
   MaterialType.from_attribute_get_enum("concrete")  # ValueError!
   MaterialType.from_attribute_get_enum("Concrete")  # Works
   ```

2. **Return Types**: `from_name_get_enum` returns `None` on failure, but `from_attribute_get_enum` raises `ValueError`

3. **Forgetting `@unique`**: Child enums should include `@unique` decorator

4. **Non-String Values**: `_missing_()` returns `None` for non-string inputs

### Best Practices

1. **Use `@unique`**: Always decorate enum classes with `@unique`
2. **PascalCase Values**: Use PascalCase for enum values to match XMI convention
3. **UPPER_CASE Names**: Use UPPER_CASE for enum member names (Python convention)
4. **Docstrings**: Add docstrings to enum classes explaining their purpose
5. **Error Handling**: Wrap `from_attribute_get_enum` in try-except for safety

## Related Classes

### Direct Subclasses (Enums)
- `MaterialType` - Material type enumeration (Concrete, Steel, etc.)
- `SegmentType` - Geometric segment type enumeration (Line, Arc, etc.)
- `CrossSectionShape` - Cross-section shape enumeration (Rectangle, Circle, etc.)
- `MemberType` - Member type enumeration (Beam, Column, etc.)

### Python Base Classes
- `Enum` - Python's base enumeration class
- `str` - Python string type for serialization

### Pydantic Integration
- `BaseModel` - Uses enums as field types
- `Field` - Field definition supporting enum validation
- `field_validator` - Custom validators for enum conversion

### Entity Classes Using Enums
- [`XmiStructuralMaterial`](../entities/XmiStructuralMaterial.md) - Uses MaterialType enum
- [`XmiSegment`](../entities/XmiSegment.md) - Uses SegmentType enum
- [`XmiCrossSection`](../entities/XmiCrossSection.md) - Uses CrossSectionShape enum

## Examples of Real XMI Enums

### MaterialType

```python
@unique
class MaterialType(XmiBaseEnum):
    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    ALUMINUM = "Aluminum"
    MASONRY = "Masonry"
    OTHER = "Other"
```

### SegmentType

```python
@unique
class SegmentType(XmiBaseEnum):
    LINE = "Line"
    CIRCULAR_ARC = "CircularArc"
    PARABOLIC_ARC = "ParabolicArc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
```

### CrossSectionShape

```python
@unique
class CrossSectionShape(XmiBaseEnum):
    RECTANGLE = "Rectangle"
    CIRCLE = "Circle"
    I_SECTION = "ISection"
    T_SECTION = "TSection"
    L_SECTION = "LSection"
    CHANNEL = "Channel"
    CUSTOM = "Custom"
```
