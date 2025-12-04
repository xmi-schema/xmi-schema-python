# PLAN.md - XMI Schema Python Library Documentation & Testing Plan

## Current State Assessment

### Existing State
- **Python files**: 37 files in v1, 37 files in v2 (74 total)
- **Entity classes**: 8 entity classes per version (16 total)
- **Test files**: 48 existing test files
- **Docstrings**: Minimal (~6 occurrences in v1, status unknown for v2)
- **README files**: No per-class README files exist in src/xmi/
- **Test coverage**: Partial - some entities have tests, coverage unknown

### Gaps Identified
1. ❌ Many model classes lack comprehensive unit tests
2. ❌ No per-class README documentation with property definitions
3. ❌ Most functions lack docstrings
4. ❌ Incomplete test coverage across all entity types, enums, geometries, and relationships

---

## Goals

### 1. Complete Unit Test Coverage
Add comprehensive unit tests for every model class across both v1 and v2 implementations, ensuring all properties, methods, and edge cases are tested.

### 2. Per-Class Documentation
Create README.md files for each XMI class with detailed property definitions, usage examples, and relationship explanations.

### 3. Function-Level Documentation
Add comprehensive docstrings to all Python functions following Google or NumPy docstring conventions.

### 4. Test Organization
Ensure all unit tests are properly organized within the `tests/` directory structure mirroring the `src/` structure.

---

## Detailed Implementation Plan

## Phase 1: Unit Testing for Model Classes

### 1.1 Test Coverage Audit
**Action**: Identify which model classes lack tests or have incomplete coverage.

**Steps**:
1. List all entity classes in v1 and v2:
   - v1: `src/xmi/v1/entities/*.py`
   - v2: `src/xmi/v2/Models/entities/*.py`
2. List all geometry classes:
   - v1: `src/xmi/v1/geometries/*.py`
   - v2: `src/xmi/v2/Models/geometries/*.py`
3. List all relationship classes:
   - v1: `src/xmi/v1/relationships/*.py`
   - v2: `src/xmi/v2/Models/relationships/*.py`
4. List all enum classes:
   - v1: `src/xmi/v1/enums/*.py`
   - v2: `src/xmi/v2/Models/enums/*.py`
5. Cross-reference with existing tests in `tests/xmi/v1/` and `tests/xmi/v2/`
6. Create a checklist of missing tests

### 1.2 Test Structure Plan
**Directory Structure**:
```
tests/
├── xmi/
│   ├── v1/
│   │   ├── test_entities/          # Entity class tests
│   │   ├── test_geometries/        # Geometry class tests
│   │   ├── test_relationships/     # Relationship class tests
│   │   ├── test_enums/            # Enum class tests
│   │   ├── test_scripts/          # Integration tests (existing)
│   │   └── test_inputs/           # Test data files
│   └── v2/
│       ├── test_entities/          # Already exists
│       ├── test_geometries/        # Already exists
│       ├── test_relationships/     # Already exists
│       ├── test_enums/            # Already exists
│       ├── test_models/           # XmiModel & XmiManager tests
│       └── test_inputs/           # Test data files
```

### 1.3 Test Implementation for Each Class Type

#### A. Entity Tests
For each entity class, create tests covering:
- ✅ **Initialization**: Test valid initialization with all parameters
- ✅ **Property setters/getters**: Test all properties with valid/invalid values
- ✅ **Type validation**: Test TypeError exceptions for wrong types
- ✅ **Value validation**: Test ValueError exceptions for invalid values
- ✅ **from_xmi_dict_obj()** method (v1) or **from_dict()** (v2): Test parsing from dictionaries
- ✅ **to_dict()** method: Test serialization
- ✅ **Edge cases**: None values, empty strings, boundary values

**Entity Classes to Test** (both v1 and v2):
- `XmiSegment`
- `XmiCrossSection`
- `XmiStructuralCurveMember`
- `XmiStructuralMaterial`
- `XmiStructuralPointConnection`
- `XmiStorey`
- `XmiStructuralSurfaceMember`
- `XmiUnit`

**Test Template**:
```python
def test_entity_init_valid():
    """Test successful initialization with valid parameters."""
    pass

def test_entity_init_missing_required():
    """Test initialization fails when required parameters are missing."""
    pass

def test_entity_property_validation():
    """Test property setters validate types and values correctly."""
    pass

def test_entity_from_dict():
    """Test creation from dictionary representation."""
    pass

def test_entity_to_dict():
    """Test serialization to dictionary."""
    pass
```

#### B. Geometry Tests
For each geometry class:
- ✅ Test initialization with valid coordinates
- ✅ Test invalid coordinate types/values
- ✅ Test geometric calculations (if any)
- ✅ Test relationships with XmiPoint3D

**Geometry Classes to Test**:
- `XmiPoint3D`
- `XmiLine3D`
- `XmiArc3D`
- `XmiBaseGeometry`

#### C. Relationship Tests
For each relationship class:
- ✅ Test initialization with valid source/target entities
- ✅ Test TypeError when source/target are not XmiBaseEntity
- ✅ Test relationship name validation
- ✅ Test relationship-specific attributes (is_begin, is_end, etc.)

**Relationship Classes to Test**:
- `XmiHasGeometry`
- `XmiHasStructuralMaterial`
- `XmiHasCrossSection`
- `XmiHasStructuralNode`
- `XmiHasSegment`
- `XmiHasPoint3D`
- `XmiHasLine3D`

#### D. Enum Tests
For each enum class:
- ✅ Test all enum values are accessible
- ✅ Test `from_attribute_get_enum()` method (if exists)
- ✅ Test invalid value handling

**Enum Classes to Test**:
- `XmiSegmentTypeEnum`
- `XmiShapeEnum`
- `XmiUnitEnum`
- `XmiStructuralCurveMemberSystemLineEnum`
- `XmiStructuralCurveMemberTypeEnum`
- `XmiMaterialTypeEnum`
- `XmiStructuralSurfaceMemberTypeEnum`
- `XmiStructuralSurfaceMemberSpanTypeEnum`
- `XmiStructuralSurfaceMemberSystemPlaneEnum`

#### E. Manager & Model Tests
- ✅ Test `XmiManager.read_xmi_dict()` with valid/invalid input
- ✅ Test `XmiModel.create_entity()`
- ✅ Test `XmiModel.create_relationship()`
- ✅ Test `XmiModel.find_relationships_by_source()`
- ✅ Test `XmiModel.find_relationships_by_target()`
- ✅ Test error logging in ErrorLog
- ✅ Test dependency order enforcement

### 1.4 Test Data Management
**Action**: Create reusable test fixtures and input data

**Steps**:
1. Create `conftest.py` files at appropriate levels with common fixtures
2. Create test input JSON files in `test_inputs/` directories
3. Create factory functions for commonly used test objects
4. Document test data format and structure

---

## Phase 2: Per-Class README Documentation

### 2.1 Documentation Structure
**Location**: Create README.md files within each class directory

**Structure**:
```
src/xmi/v1/entities/
├── xmi_material.py
├── XmiStructuralMaterial.md          # New
├── xmi_structural_cross_section.py
├── XmiCrossSection.md      # New
└── ...

src/xmi/v2/Models/entities/
├── xmi_material.py
├── XmiStructuralMaterial.md          # New
└── ...
```

### 2.2 README Template for Each Class

Each class README should contain:

```markdown
# [ClassName] (e.g., XmiStructuralMaterial)

## Overview
Brief description of what this class represents in the XMI schema and its purpose.

## Class Hierarchy
- Parent: [ParentClass]
- Implements: [Interfaces if any]

## Properties

### Required Properties
| Property | Type | Description | Validation |
|----------|------|-------------|------------|
| property_name | Type | Description | Constraints |

### Optional Properties
| Property | Type | Default | Description | Validation |
|----------|------|---------|-------------|------------|
| property_name | Type | None | Description | Constraints |

## Relationships
List of relationships this entity participates in:
- **Has[RelationType]**: Description of relationship

## Usage Examples

### Creating an Instance
```python
# Example code
```

### Loading from Dictionary
```python
# Example code
```

### Common Patterns
```python
# Example code showing typical usage
```

## Validation Rules
- List of validation rules enforced by the class
- Type constraints
- Value constraints
- Dependency requirements

## Notes
- Any special considerations
- Known limitations
- Version-specific differences (v1 vs v2)

## Related Classes
- Links to related entity documentation
```

### 2.3 Documentation Priority Order

**High Priority** (Core entities users interact with directly):
1. `XmiStructuralMaterial`
2. `XmiStructuralPointConnection`
3. `XmiCrossSection`
4. `XmiStructuralCurveMember`
5. `XmiStructuralSurfaceMember`
6. `XmiManager`
7. `XmiModel`

**Medium Priority** (Supporting classes):
1. `XmiSegment`
2. `XmiPoint3D`
3. `XmiLine3D`
4. `XmiArc3D`
5. `XmiUnit`
6. `XmiStorey`

**Lower Priority** (Base classes and relationships):
1. `XmiBaseEntity`
2. `XmiBaseRelationship`
3. All relationship classes
4. All enum classes

### 2.4 Documentation Implementation Steps

For each class:
1. ✅ Analyze the class implementation (properties, methods, validation)
2. ✅ Review existing tests to understand expected behavior
3. ✅ Create the README.md file using the template
4. ✅ Add usage examples with actual working code
5. ✅ Document all properties with types and validation rules
6. ✅ Cross-reference with related classes
7. ✅ Review and verify accuracy

---

## Phase 3: Docstring Documentation

### 3.1 Docstring Convention
**Standard**: Use **Google Style** docstrings for consistency

**Example**:
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """Brief one-line description.

    Detailed description of what the function does, if needed.
    Can span multiple lines.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised

    Example:
        >>> function_name(value1, value2)
        expected_output
    """
    pass
```

### 3.2 Documentation Scope

#### A. Class Docstrings
Every class should have:
```python
class ClassName(BaseClass):
    """Brief description of the class.

    Detailed description of the class purpose, its role in the XMI schema,
    and how it relates to other classes.

    Attributes:
        attr1: Description
        attr2: Description

    Example:
        >>> obj = ClassName(param1, param2)
        >>> obj.method()
    """
```

#### B. Method/Function Docstrings
Every public method should have:
- Brief description
- Args section
- Returns section
- Raises section (if applicable)
- Example (for complex methods)

#### C. Property Docstrings
Properties should have:
```python
@property
def property_name(self) -> Type:
    """Brief description of what this property represents.

    Returns:
        Description of the value returned
    """
    return self._property_name

@property_name.setter
def property_name(self, value: Type) -> None:
    """Set the property value with validation.

    Args:
        value: Description and constraints

    Raises:
        TypeError: If value is not of expected type
        ValueError: If value fails validation
    """
    self._property_name = value
```

### 3.3 Docstring Implementation Plan

**Phase 3A: Core Classes** (Week 1)
1. `XmiManager` and `XmiModel`
2. `XmiBaseEntity` and `XmiBaseRelationship`
3. All entity classes (8 per version = 16 total)

**Phase 3B: Supporting Classes** (Week 2)
1. All geometry classes (3 per version = 6 total)
2. All relationship classes (~8 per version = 16 total)
3. All enum classes (~9 per version = 18 total)

**Phase 3C: Utility & Helper Functions** (Week 3)
1. `xmi_utilities.py`
2. `xmi_errors.py`
3. `xmi_entity_type_mapping.py` (v2)
4. Helper functions in base classes

### 3.4 Docstring Quality Checklist
For each function/method:
- [ ] Has a brief one-line summary
- [ ] Lists all parameters with types and descriptions
- [ ] Documents return value with type
- [ ] Lists all possible exceptions
- [ ] Includes usage example for complex functions
- [ ] Uses consistent formatting
- [ ] Is grammatically correct

---

## Phase 4: Test Organization & Validation

### 4.1 Test Organization Standards

**Naming Convention**:
- Test files: `test_[module_name].py`
- Test functions: `test_[class_name]_[scenario]`
- Test classes: `Test[ClassName]` (if grouping related tests)

**Example**:
```python
# File: tests/xmi/v1/test_entities/test_xmi_material.py

def test_xmi_material_init_valid():
    """Test XmiStructuralMaterial initialization with valid parameters."""
    pass

def test_xmi_material_init_missing_type():
    """Test XmiStructuralMaterial raises error when material_type is missing."""
    pass

class TestXmiStructuralMaterialValidation:
    """Group of tests for XmiStructuralMaterial validation logic."""

    def test_unit_weight_validation(self):
        """Test unit_weight property validates numeric values."""
        pass
```

### 4.2 Test File Organization

Ensure tests mirror source structure:
```
src/xmi/v1/entities/xmi_material.py
→ tests/xmi/v1/test_entities/test_xmi_material.py

src/xmi/v2/Models/geometries/xmi_point_3d.py
→ tests/xmi/v2/test_geometries/test_xmi_point_3d.py
```

### 4.3 Test Input Data Organization

**Structure**:
```
tests/xmi/v1/test_inputs/
├── xmi_manager/              # Integration test data
│   └── xmi_structural_manager_test_1.json
├── entities/                 # Per-entity test data
│   ├── material_valid.json
│   ├── material_invalid.json
│   └── cross_section_valid.json
└── fixtures/                 # Shared test fixtures
    └── common_fixtures.py
```

### 4.4 Validation Steps

After implementation:
1. ✅ Run `pytest --cov=src/xmi tests/` to check coverage
2. ✅ Target minimum 80% code coverage per module
3. ✅ Ensure all tests pass in both v1 and v2
4. ✅ Verify test isolation (tests don't depend on each other)
5. ✅ Check test performance (no slow tests without markers)
6. ✅ Validate test documentation

---

## Implementation Timeline

### Week 1-2: Testing Foundation
- [ ] Complete test coverage audit
- [ ] Create missing test files with placeholders
- [ ] Implement tests for all v1 entities
- [ ] Implement tests for all v1 geometries

### Week 3-4: Complete Test Suite
- [ ] Implement tests for all v2 entities
- [ ] Implement tests for all v2 geometries
- [ ] Implement tests for all relationship classes
- [ ] Implement tests for all enum classes
- [ ] Add integration tests for XmiManager/XmiModel

### Week 5-6: Documentation (README)
- [ ] Create README templates
- [ ] Document high-priority classes (Manager, Model, core entities)
- [ ] Document medium-priority classes
- [ ] Document lower-priority classes
- [ ] Review and cross-link documentation

### Week 7-8: Docstrings
- [ ] Add docstrings to core classes (Manager, Model, Base)
- [ ] Add docstrings to all entity classes
- [ ] Add docstrings to geometry and relationship classes
- [ ] Add docstrings to enum and utility classes
- [ ] Review and validate docstring consistency

### Week 9: Final Review & Validation
- [ ] Run full test suite with coverage report
- [ ] Review all documentation for accuracy
- [ ] Update main README.md with links to class documentation
- [ ] Create documentation index
- [ ] Final quality check

---

## Success Criteria

### Testing Success Criteria
- ✅ All entity classes have comprehensive unit tests
- ✅ All geometry classes have comprehensive unit tests
- ✅ All relationship classes have comprehensive unit tests
- ✅ All enum classes have comprehensive unit tests
- ✅ Code coverage ≥80% for all modules
- ✅ All tests pass consistently
- ✅ Test execution time <2 minutes

### Documentation Success Criteria
- ✅ Every XMI class has a dedicated README.md
- ✅ All properties are documented with types and validation rules
- ✅ All classes have usage examples
- ✅ All functions have Google-style docstrings
- ✅ Documentation is accurate and up-to-date
- ✅ Users can understand how to use any class from documentation alone

### Organization Success Criteria
- ✅ Tests are properly organized in `tests/` directory
- ✅ Test file naming follows conventions
- ✅ Test structure mirrors source structure
- ✅ Test data is organized and reusable
- ✅ Documentation is easily discoverable

---

## Tools & Automation

### Recommended Tools
1. **pytest-cov**: For code coverage reporting
   ```bash
   pip install pytest-cov
   pytest --cov=src/xmi tests/ --cov-report=html
   ```

2. **interrogate**: For docstring coverage checking
   ```bash
   pip install interrogate
   interrogate src/xmi -v
   ```

3. **pydocstyle**: For docstring style validation
   ```bash
   pip install pydocstyle
   pydocstyle src/xmi
   ```

### CI/CD Integration
Add to GitHub Actions workflow:
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src/xmi tests/ --cov-report=xml

- name: Check docstring coverage
  run: |
    interrogate src/xmi --fail-under=80
```

---

## Maintenance Plan

### Ongoing Requirements
1. **New Classes**: When adding new XMI classes:
   - [ ] Create unit tests before or alongside implementation
   - [ ] Create README.md documentation
   - [ ] Add comprehensive docstrings
   - [ ] Update entity type mappings
   - [ ] Update main documentation index

2. **Existing Classes**: When modifying existing classes:
   - [ ] Update relevant unit tests
   - [ ] Update README.md if properties change
   - [ ] Update docstrings if signatures change
   - [ ] Verify all tests still pass

3. **Documentation Review**: Quarterly
   - [ ] Review documentation accuracy
   - [ ] Update examples if API changes
   - [ ] Fix broken links
   - [ ] Improve clarity based on user feedback

---

## Notes & Considerations

### Version Differences (v1 vs v2)
- v1 uses `__slots__` and manual validation
- v2 uses Pydantic models with automatic validation
- Test strategies may differ slightly between versions
- Documentation should highlight version-specific differences

### Test Data Strategy
- Use realistic XMI data from actual use cases
- Create minimal examples for unit tests
- Create comprehensive examples for integration tests
- Keep test data files small and focused

### Documentation Accessibility
- Consider generating HTML documentation with Sphinx
- Ensure documentation works well in GitHub markdown viewer
- Consider adding a documentation site (Read the Docs, GitHub Pages)

---

## Getting Started

To begin implementation:

1. **Start with testing audit**:
   ```bash
   # Generate current coverage report
   pytest --cov=src/xmi tests/ --cov-report=html
   # Open htmlcov/index.html to see gaps
   ```

2. **Pick a class to document**:
   - Start with `XmiStructuralMaterial` (simplest entity)
   - Create tests first, then README, then docstrings
   - Use as template for other classes

3. **Establish patterns**:
   - Create templates for tests, READMEs, docstrings
   - Get feedback on first complete example
   - Apply pattern to remaining classes

4. **Track progress**:
   - Create GitHub issues for each major component
   - Use checklist in this document
   - Regular progress reviews
