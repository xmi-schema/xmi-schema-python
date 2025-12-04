# XMI Schema Python v2 - Feature Parity Game Plan

## Executive Summary

**Current Status**: Python v2 has ~67% feature parity with C# v0.8.0

**Goal**: Achieve 95%+ feature parity to enable full interoperability between physical design models and analytical representations

**Priority**: The Python library needs to support the same entity types, relationships, and architectural patterns as the C# implementation to be a viable cross-platform alternative.

---

## Gap Analysis Summary

### Critical Missing Features (HIGH PRIORITY)

1. **Physical Entity Layer** - 4 entity classes missing
   - XmiBeam (physical horizontal structural member)
   - XmiColumn (physical vertical structural member)
   - XmiSlab (physical horizontal plate element)
   - XmiWall (physical vertical plate element)

2. **Physical-to-Analytical Bridge** - 1 relationship missing
   - XmiHasStructuralCurveMember (links physical to analytical entities)

3. **Base Class Architecture** - 2 base classes missing
   - XmiBasePhysicalEntity (auto-assigns "Physical" classification)
   - XmiBaseStructuralAnalyticalEntity (auto-assigns "StructuralAnalytical" classification)

### Medium Priority Features

4. **Coordinate Deduplication** - Memory optimization
   - Factory method: XmiModel.CreatePoint3D()
   - Eliminates duplicate 3D coordinates in large models

5. **Type Classification System** - Automatic domain typing
   - Physical vs Analytical vs Geometry classification via inheritance

### Low Priority Features

6. **Graph Integration** - Advanced queries (may not be needed)
   - C# uses QuikGraph for graph operations
   - Current relationship system may be sufficient

7. **Enum Value Audit** - Ensure complete alignment
   - Verify all enum values match C# exactly

---

## Implementation Roadmap

### Phase 1: Foundation - Base Class Architecture (Week 1)

**Goal**: Establish proper inheritance hierarchy for domain separation

#### Task 1.1: Create XmiBasePhysicalEntity
- **File**: `src/xmi/v2/models/bases/xmi_base_physical_entity.py`
- **Inherits**: XmiBaseEntity
- **Auto-assigns**: entity_type = "Physical"
- **Properties**: Same as XmiBaseEntity
- **Tests**: `tests/xmi/v2/test_entities/test_xmi_base_physical_entity.py`

#### Task 1.2: Create XmiBaseStructuralAnalyticalEntity
- **File**: `src/xmi/v2/models/bases/xmi_base_structural_analytical_entity.py`
- **Inherits**: XmiBaseEntity
- **Auto-assigns**: entity_type = "StructuralAnalytical"
- **Properties**: Same as XmiBaseEntity
- **Tests**: `tests/xmi/v2/test_entities/test_xmi_base_structural_analytical_entity.py`

#### Task 1.3: Refactor Existing Analytical Entities
- **Update to inherit from XmiBaseStructuralAnalyticalEntity**:
  - XmiStructuralCurveMember
  - XmiStructuralSurfaceMember
  - XmiStructuralPointConnection
  - XmiStructuralStorey
- **Verify**: Automatic entity_type assignment works
- **Tests**: Update existing test files to verify new inheritance

#### Task 1.4: Update Base Class Exports
- **File**: `src/xmi/v2/models/bases/__init__.py`
- **Add**: XmiBasePhysicalEntity, XmiBaseStructuralAnalyticalEntity
- **Verify**: All imports work correctly

**Deliverable**: Proper base class hierarchy with automatic type classification

**Estimated Effort**: 2-3 days

---

### Phase 2: Physical Entity Implementation (Week 2)

**Goal**: Create 4 physical entity classes matching C# implementation

#### Task 2.1: Implement XmiBeam
- **File**: `src/xmi/v2/models/entities/xmi_beam.py`
- **Inherits**: XmiBasePhysicalEntity
- **Properties** (to match C# version):
  - Inherited: id, name, ifcguid, native_id, description, entity_type
  - Beam-specific properties (TBD based on C# implementation)
- **Methods**:
  - from_dict() for parsing
  - Pydantic validators
- **Test File**: `tests/xmi/v2/test_entities/test_xmi_beam.py`
- **Test Cases**:
  - Basic instantiation
  - from_dict() parsing
  - Validation of required/optional fields
  - Serialization round-trip

#### Task 2.2: Implement XmiColumn
- **File**: `src/xmi/v2/models/entities/xmi_column.py`
- **Inherits**: XmiBasePhysicalEntity
- **Properties**: Similar structure to XmiBeam
- **Test File**: `tests/xmi/v2/test_entities/test_xmi_column.py`
- **Test Cases**: Same pattern as XmiBeam

#### Task 2.3: Implement XmiSlab
- **File**: `src/xmi/v2/models/entities/xmi_slab.py`
- **Inherits**: XmiBasePhysicalEntity
- **Properties**: Surface-based physical properties
- **Test File**: `tests/xmi/v2/test_entities/test_xmi_slab.py`
- **Test Cases**: Same pattern as XmiBeam

#### Task 2.4: Implement XmiWall
- **File**: `src/xmi/v2/models/entities/xmi_wall.py`
- **Inherits**: XmiBasePhysicalEntity
- **Properties**: Vertical surface physical properties
- **Test File**: `tests/xmi/v2/test_entities/test_xmi_wall.py`
- **Test Cases**: Same pattern as XmiBeam

#### Task 2.5: Update Entity Exports
- **File**: `src/xmi/v2/models/entities/__init__.py`
- **Add**: XmiBeam, XmiColumn, XmiSlab, XmiWall exports

**Deliverable**: 4 fully tested physical entity classes

**Estimated Effort**: 4-5 days

**Dependencies**: Phase 1 must be complete

---

### Phase 3: Physical-to-Analytical Relationship (Week 2-3)

**Goal**: Create bridge between physical design model and analytical model

#### Task 3.1: Implement XmiHasStructuralCurveMember Relationship
- **File**: `src/xmi/v2/models/relationships/xmi_has_structural_curve_member.py`
- **Inherits**: XmiBaseRelationship
- **Source**: Physical entities (XmiBeam, XmiColumn)
- **Target**: Analytical entity (XmiStructuralCurveMember)
- **Properties**:
  - Inherited: id, source, target, name, description, entity_type, uml_type
  - Relationship-specific properties (if any in C#)
- **Validation**:
  - Ensure source is XmiBasePhysicalEntity
  - Ensure target is XmiStructuralCurveMember
- **Test File**: `tests/xmi/v2/test_relationships/test_xmi_has_structural_curve_member.py`
- **Test Cases**:
  - Valid relationship creation (Beam → CurveMember)
  - Valid relationship creation (Column → CurveMember)
  - Invalid source/target validation
  - Serialization round-trip

#### Task 3.2: Update Relationship Exports
- **File**: `src/xmi/v2/models/relationships/__init__.py`
- **Add**: XmiHasStructuralCurveMember export

**Deliverable**: Fully tested physical-to-analytical relationship

**Estimated Effort**: 1-2 days

**Dependencies**: Phase 2 must be complete

---

### Phase 4: Entity Type Mapping Integration (Week 3)

**Goal**: Register new entities and relationships in the mapping system

#### Task 4.1: Update ENTITY_CLASS_MAPPING
- **File**: `src/xmi/v2/utils/xmi_entity_type_mapping.py`
- **Add to mapping**:
  ```python
  "XmiBeam": XmiBeam,
  "XmiColumn": XmiColumn,
  "XmiSlab": XmiSlab,
  "XmiWall": XmiWall,
  ```
- **Add imports** for new entity classes

#### Task 4.2: Update RELATIONSHIP_CLASS_MAPPING
- **File**: `src/xmi/v2/utils/xmi_entity_type_mapping.py`
- **Add to mapping**:
  ```python
  "XmiHasStructuralCurveMember": XmiHasStructuralCurveMember,
  ```
- **Add import** for new relationship class

#### Task 4.3: Update XmiModel.load_from_dict()
- **File**: `src/xmi/v2/models/xmi_model/xmi_model.py`
- **Verify**: New entities are properly instantiated from dictionaries
- **Test**: Create integration test with physical entities
- **Test File**: `tests/xmi/v2/test_xmi_model/test_xmi_model_physical_entities.py`

**Deliverable**: Full integration of new entities into loading/parsing system

**Estimated Effort**: 1 day

**Dependencies**: Phases 2 and 3 must be complete

---

### Phase 5: Coordinate Deduplication (Week 4)

**Goal**: Implement memory-efficient coordinate management

#### Task 5.1: Implement XmiModel.create_point_3d()
- **File**: `src/xmi/v2/models/xmi_model/xmi_model.py`
- **Method**: create_point_3d(x: float, y: float, z: float, tolerance: float = 1e-6) -> XmiPoint3D
- **Logic**:
  - Maintain internal dictionary of coordinates
  - Check if coordinate already exists within tolerance
  - Return existing point if found, create new if not
- **Properties**:
  - _point_cache: Dict[Tuple[float, float, float], XmiPoint3D] = {}
  - _point_tolerance: float = 1e-6

#### Task 5.2: Implement Tolerance-Aware Equality
- **File**: `src/xmi/v2/models/geometries/xmi_point_3d.py`
- **Add method**: equals_within_tolerance(other: XmiPoint3D, tolerance: float) -> bool
- **Update**: __eq__ to support tolerance comparison

#### Task 5.3: Update Entity Parsing to Use Factory
- **Files to update**:
  - XmiStructuralPointConnection.from_dict()
  - Any entity that creates XmiPoint3D objects
- **Change**: Use xmi_model.create_point_3d() instead of direct XmiPoint3D()

#### Task 5.4: Create Tests
- **Test File**: `tests/xmi/v2/test_xmi_model/test_coordinate_deduplication.py`
- **Test Cases**:
  - Duplicate coordinates are deduplicated
  - Tolerance parameter works correctly
  - Memory usage is reduced with large models
  - Factory method maintains referential integrity

**Deliverable**: Memory-efficient coordinate management

**Estimated Effort**: 2-3 days

**Dependencies**: None (can be done in parallel with other phases)

---

### Phase 6: Testing and Documentation (Week 4-5)

**Goal**: Comprehensive testing and documentation of new features

#### Task 6.1: Integration Tests
- **File**: `tests/xmi/v2/test_integration/test_physical_analytical_bridge.py`
- **Test Scenarios**:
  - Create physical beam with analytical curve member
  - Create physical column with analytical curve member
  - Create physical slab (verify no curve member relationship)
  - Create physical wall (verify no curve member relationship)
  - Round-trip serialization (dict → objects → dict)
  - Error handling for invalid relationships

#### Task 6.2: End-to-End Tests
- **File**: `tests/xmi/v2/test_integration/test_complete_model.py`
- **Test Scenario**: Complete building model with:
  - Materials
  - Cross-sections
  - Physical beams, columns, slabs, walls
  - Analytical curve members and surface members
  - Physical-to-analytical relationships
  - Point connections and geometry
  - Verify all relationships are correctly created

#### Task 6.3: Create Test Input Files
- **Directory**: `tests/xmi/v2/test_inputs/`
- **Files needed**:
  - `physical_beam_test.json` - Sample XmiBeam data
  - `physical_column_test.json` - Sample XmiColumn data
  - `physical_slab_test.json` - Sample XmiSlab data
  - `physical_wall_test.json` - Sample XmiWall data
  - `complete_physical_model.json` - Full building model

#### Task 6.4: Update Documentation
- **File**: `CLAUDE.md`
- **Updates needed**:
  - Add physical entity section
  - Document XmiHasStructuralCurveMember relationship
  - Update base class hierarchy diagram
  - Add physical-to-analytical mapping patterns
  - Update version comparison table

#### Task 6.5: Create Entity Documentation
- **Files to create**:
  - `docs/entities/XmiBeam.md`
  - `docs/entities/XmiColumn.md`
  - `docs/entities/XmiSlab.md`
  - `docs/entities/XmiWall.md`
  - `docs/relationships/XmiHasStructuralCurveMember.md`

#### Task 6.6: Update README
- **File**: `README.md`
- **Add**: Feature parity statement
- **Add**: Physical entity examples
- **Update**: Version number and changelog

**Deliverable**: Fully tested and documented new features

**Estimated Effort**: 3-4 days

**Dependencies**: All previous phases complete

---

### Phase 7: C# Reference Analysis (Week 5)

**Goal**: Deep dive into C# implementation to ensure exact feature parity

#### Task 7.1: Clone and Analyze C# Repository
- **Repository**: https://github.com/xmi-schema/xmi-schema-csharp
- **Focus Areas**:
  - Physical entity properties (exact fields)
  - Relationship properties and validation rules
  - Serialization format
  - Error handling patterns

#### Task 7.2: Property Mapping Verification
- **Create**: Property comparison spreadsheet
- **Document**: Exact property names, types, defaults for:
  - XmiBeam
  - XmiColumn
  - XmiSlab
  - XmiWall
  - XmiHasStructuralCurveMember

#### Task 7.3: Update Python Implementation
- **Adjust**: Python entities to match C# exactly
- **Ensure**: Field names, types, defaults align
- **Verify**: Serialization format compatibility

#### Task 7.4: Cross-Platform Testing
- **Create**: Test cases using C# output as input to Python
- **Verify**: Python can parse C# JSON output
- **Verify**: C# can parse Python JSON output (if possible)

**Deliverable**: Verified feature parity with C# implementation

**Estimated Effort**: 3-4 days

**Dependencies**: Phases 1-6 should be complete first

---

### Phase 8: Performance and Optimization (Week 6)

**Goal**: Ensure Python implementation is performant and production-ready

#### Task 8.1: Benchmark Testing
- **Create**: Performance benchmarks
- **Metrics**:
  - Model loading time (various sizes)
  - Memory usage
  - Relationship query performance
  - Serialization/deserialization speed

#### Task 8.2: Memory Profiling
- **Tool**: memory_profiler
- **Test**: Large models (1000+ entities)
- **Verify**: Coordinate deduplication works
- **Identify**: Memory bottlenecks

#### Task 8.3: Optimization
- **Areas to optimize**:
  - Relationship queries (indexing)
  - Entity lookup (caching)
  - Serialization (bulk operations)
- **Implement**: Lazy loading if needed

**Deliverable**: Production-ready performance

**Estimated Effort**: 2-3 days

**Dependencies**: All previous phases complete

---

## Required File Structure Changes

### New Files to Create

```
src/xmi/v2/models/
├── bases/
│   ├── xmi_base_physical_entity.py (NEW)
│   └── xmi_base_structural_analytical_entity.py (NEW)
├── entities/
│   ├── xmi_beam.py (NEW)
│   ├── xmi_column.py (NEW)
│   ├── xmi_slab.py (NEW)
│   └── xmi_wall.py (NEW)
└── relationships/
    └── xmi_has_structural_curve_member.py (NEW)

tests/xmi/v2/
├── test_entities/
│   ├── test_xmi_base_physical_entity.py (NEW)
│   ├── test_xmi_base_structural_analytical_entity.py (NEW)
│   ├── test_xmi_beam.py (NEW)
│   ├── test_xmi_column.py (NEW)
│   ├── test_xmi_slab.py (NEW)
│   └── test_xmi_wall.py (NEW)
├── test_relationships/
│   └── test_xmi_has_structural_curve_member.py (NEW)
├── test_integration/
│   ├── test_physical_analytical_bridge.py (NEW)
│   └── test_complete_model.py (NEW)
├── test_inputs/
│   ├── physical_beam_test.json (NEW)
│   ├── physical_column_test.json (NEW)
│   ├── physical_slab_test.json (NEW)
│   ├── physical_wall_test.json (NEW)
│   └── complete_physical_model.json (NEW)
└── test_xmi_model/
    └── test_coordinate_deduplication.py (NEW)

docs/
├── entities/
│   ├── XmiBeam.md (NEW)
│   ├── XmiColumn.md (NEW)
│   ├── XmiSlab.md (NEW)
│   └── XmiWall.md (NEW)
└── relationships/
    └── XmiHasStructuralCurveMember.md (NEW)
```

### Files to Modify

```
src/xmi/v2/models/
├── bases/__init__.py (UPDATE - add new base classes)
├── entities/__init__.py (UPDATE - add new entities)
├── relationships/__init__.py (UPDATE - add new relationship)
└── xmi_model/xmi_model.py (UPDATE - add create_point_3d())

src/xmi/v2/utils/
└── xmi_entity_type_mapping.py (UPDATE - add new mappings)

src/xmi/v2/models/entities/
├── xmi_structural_curve_member.py (UPDATE - inherit from new base)
├── xmi_structural_surface_member.py (UPDATE - inherit from new base)
├── xmi_structural_point_connection.py (UPDATE - inherit from new base)
└── xmi_structural_storey.py (UPDATE - inherit from new base)

CLAUDE.md (UPDATE - document new features)
README.md (UPDATE - update features and examples)
```

---

## Testing Strategy

### Unit Tests (Per Entity/Relationship)
- Basic instantiation
- from_dict() parsing
- Field validation (required/optional)
- Type validation
- Serialization round-trip
- Error handling

### Integration Tests
- Physical-to-analytical relationships
- Complete model loading
- Cross-entity references
- Relationship queries

### End-to-End Tests
- Complete building model scenarios
- Multi-entity workflows
- Error accumulation
- Performance with large models

### Cross-Platform Tests
- Parse C# JSON output
- Verify field mapping
- Serialization compatibility

---

## Success Criteria

### Phase 1-3 (Core Implementation)
- [ ] XmiBasePhysicalEntity created and tested
- [ ] XmiBaseStructuralAnalyticalEntity created and tested
- [ ] All 4 analytical entities refactored to new base class
- [ ] XmiBeam, XmiColumn, XmiSlab, XmiWall fully implemented
- [ ] XmiHasStructuralCurveMember relationship implemented
- [ ] All unit tests passing
- [ ] Integration tests passing

### Phase 4 (Integration)
- [ ] New entities registered in mapping dictionaries
- [ ] XmiModel.load_from_dict() works with physical entities
- [ ] Round-trip serialization works

### Phase 5 (Optimization)
- [ ] Coordinate deduplication factory implemented
- [ ] Memory usage reduced in large models
- [ ] Tolerance-aware equality works

### Phase 6 (Testing & Docs)
- [ ] All test coverage >90%
- [ ] Documentation complete
- [ ] Examples created
- [ ] CLAUDE.md updated

### Phase 7 (C# Parity)
- [ ] Property mapping verified against C#
- [ ] Field types and names match exactly
- [ ] Serialization format compatible
- [ ] Cross-platform tests passing

### Phase 8 (Performance)
- [ ] Benchmarks established
- [ ] Performance acceptable for large models
- [ ] Memory usage optimized

---

## Risk Assessment

### High Risk
- **C# Property Mismatch**: Properties in C# may differ from assumptions
  - Mitigation: Early C# analysis (Phase 7 can be moved earlier)
  - Impact: Rework of entity classes

- **Breaking Changes**: Refactoring base classes may break existing code
  - Mitigation: Thorough testing of existing entities
  - Impact: Fix existing tests and user code

### Medium Risk
- **Performance Issues**: Coordinate deduplication may slow parsing
  - Mitigation: Make factory method optional
  - Impact: Users can opt-in/out

- **Relationship Complexity**: Physical-to-analytical mapping may be complex
  - Mitigation: Follow C# pattern exactly
  - Impact: Additional validation logic needed

### Low Risk
- **Documentation Gaps**: May miss documenting some features
  - Mitigation: Review C# docs thoroughly
  - Impact: Update docs later

---

## Dependencies and Prerequisites

### External Dependencies
- Access to C# repository (public)
- C# development environment (optional, for testing)
- Understanding of C# XMI implementation

### Internal Dependencies
- Existing v2 Pydantic infrastructure
- Existing test framework
- Existing entity/relationship patterns

### Knowledge Requirements
- Understanding of physical vs analytical structural models
- XMI schema design principles
- Pydantic validation patterns
- Graph-based data structures

---

## Rollout Strategy

### Version Numbering
- Current: v0.2.17
- After Phase 1-3: v0.3.0 (minor version bump for new entities)
- After Phase 5: v0.3.1 (patch for optimization)
- After Phase 7: v0.4.0 (minor version for C# parity)
- After Phase 8: v1.0.0 (major version for production release)

### Release Strategy
1. **Alpha Release** (After Phase 3): Physical entities available, testing only
2. **Beta Release** (After Phase 6): Full feature set, docs complete
3. **RC Release** (After Phase 7): C# parity verified
4. **Production Release** (After Phase 8): Performance validated

### Backward Compatibility
- Existing v2 code should continue to work
- New base classes are backward compatible
- Coordinate factory is optional (doesn't break existing code)

---

## Open Questions (Require C# Analysis)

1. **Physical Entity Properties**: What exact properties do XmiBeam, XmiColumn, XmiSlab, XmiWall have?
2. **Relationship Properties**: Does XmiHasStructuralCurveMember have additional properties?
3. **Validation Rules**: Are there specific validation rules for physical entities?
4. **Default Values**: What are the default values for new entity properties?
5. **Serialization Format**: What is the exact JSON format for physical entities?
6. **Edge Cases**: How does C# handle edge cases (null values, missing properties, etc.)?

These questions should be answered in **Phase 7: C# Reference Analysis**.

---

## Timeline Summary

| Phase | Duration | Dependencies | Deliverable |
|-------|----------|--------------|-------------|
| 1. Foundation | 2-3 days | None | Base class hierarchy |
| 2. Physical Entities | 4-5 days | Phase 1 | 4 entity classes |
| 3. Relationship | 1-2 days | Phase 2 | 1 relationship class |
| 4. Mapping Integration | 1 day | Phases 2-3 | Full integration |
| 5. Optimization | 2-3 days | None (parallel) | Coordinate factory |
| 6. Testing & Docs | 3-4 days | Phases 1-4 | Complete docs |
| 7. C# Analysis | 3-4 days | Phases 1-6 | Verified parity |
| 8. Performance | 2-3 days | All phases | Production ready |

**Total Estimated Time**: 4-6 weeks (with parallel work)

**Critical Path**: Phases 1 → 2 → 3 → 4 → 6 → 7 → 8

---

## Next Steps (Immediate Actions)

1. **Review this game plan** with stakeholders
2. **Clone C# repository** and begin analysis (can start immediately)
3. **Set up development branch**: `feature/physical-entities-v2`
4. **Begin Phase 1**: Base class implementation
5. **Create tracking document**: Track progress against this plan

---

## Notes

- This plan focuses on v2 implementation only (v1 is legacy)
- Coordinate deduplication (Phase 5) can be done in parallel
- C# analysis (Phase 7) can be moved earlier to reduce risk
- Performance testing (Phase 8) is final validation before v1.0.0 release

---

## Contact and Collaboration

- **Repository**: https://github.com/darellchua2/xmi-schema-python
- **C# Reference**: https://github.com/xmi-schema/xmi-schema-csharp
- **Issue Tracking**: Create GitHub issues for each phase
- **Testing Strategy**: Maintain >90% code coverage throughout

---

**Document Version**: 1.0
**Created**: 2025-12-04
**Last Updated**: 2025-12-04
**Author**: Claude Code Analysis
