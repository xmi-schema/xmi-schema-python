# Physical Entity Property Mapping (Python vs C#)

This document captures the Phase 7 property verification for the physical entities that now exist in both repositories:

- Python reference: `src/xmi/v2/models/entities/physical/*.py`
- C# reference: `Models/Entities/Physical/*.cs`

The goal is to record a column-for-column comparison so that any missing or mismatched fields are visible before expanding parity to other entity families.

## Common Base Fields

All physical entities inherit the shared metadata below via `XmiBasePhysicalEntity`.

| Property | Python (`xmi-schema-python`) | C# (`xmi-schema-csharp`) | Notes / Status |
| --- | --- | --- | --- |
| ID | `id: str` auto UUID if missing (`XmiBaseEntity.fill_defaults`) | `string Id` passed through constructor | ✅ Identical field name; Python autocreates when absent, which still round-trips to `ID` on export. |
| Name | `name: Optional[str]` default `id` | `string Name` defaults to `id` in constructor | ✅ Same semantics; both fall back to `id` when unset. |
| IFCGUID | `ifcguid: Optional[str]` | `string IfcGuid` | ✅ Matches naming when serialized (`IFCGUID`). |
| NativeId | `native_id: Optional[str]` | `string NativeId` | ✅ |
| Description | `description: Optional[str]` | `string Description` | ✅ |
| EntityType | auto-set to subclass name by validator | passed as `nameof(Class)` in base ctor | ✅ |
| Type | Enum `XmiBaseEntityDomainEnum.PHYSICAL` filled by `XmiBasePhysicalEntity.set_physical_domain_type` | Enum `XmiBaseEntityDomainEnum.Physical` argument on base ctor | ✅ Both guarantee domain = Physical. |

## XmiBeam / XmiColumn

Beams and columns share identical property sets in both languages.

| Property | Python Definition | C# Definition | Notes / Status |
| --- | --- | --- | --- |
| SystemLine | `system_line: XmiStructuralCurveMemberSystemLineEnum` parsed via `from_attribute_get_enum` | `XmiStructuralCurveMemberSystemLineEnum SystemLine` with JSON enum converter | ✅ Same enum surface. Python helper ensures PascalCase strings deserialize. |
| Length | `length: Union[float, int]` (`Field(..., alias="Length")`) | `double Length` | ✅ Accepts numeric inputs; serialized value matches. |
| LocalAxisX/Y/Z | Tuple of 3 floats with defaults `(1,0,0)/(0,1,0)/(0,0,1)`; validators parse comma strings; serializer emits comma string | `string LocalAxisX/Y/Z` storing comma-separated coordinates | ✅ Data is compatible; Python stores tuple internally but emits the identical string representation expected by C#. |
| BeginNodeXOffset / EndNodeXOffset | `float`, default `0.0` | `double`, default `0` (CLR default) | ✅ |
| BeginNodeYOffset / EndNodeYOffset | `float`, default `0.0` | `double`, default `0` | ✅ |
| BeginNodeZOffset / EndNodeZOffset | `float`, default `0.0` | `double`, default `0` | ✅ |
| End Fixities | _Not stored_ (handled by paired `XmiStructuralCurveMember`) | `string` | ✅ Physical beams intentionally omit fixity codes; structural analytical members retain them. |

**Validation helpers:** `XmiBeam.from_dict()` / `XmiColumn.from_dict()` mirror the JSON conversion done by the C# constructors, so no remaining mismatches were found.

## XmiSlab / XmiWall

Slabs and walls are metadata containers only—no bespoke fields beyond the base physical entity.

| Property | Python Definition | C# Definition | Notes / Status |
| --- | --- | --- | --- |
| (inherits base) | `XmiSlab` / `XmiWall` contain no extra attributes | Constructors forward to `XmiBasePhysicalEntity` without extra members | ✅ Nothing to reconcile; serialization is pure metadata. |

## Gaps / Follow-ups

1. Physical beams and columns now defer all fixity data to their analytical counterparts. Future parity checks should confirm that this split remains consistent in the C# repo (or document intentional divergence).
2. No additional physical metadata exists in C#. If future 0.9.x releases add more fields (e.g., profile references), repeat this exercise to keep the table current.
3. `LocalAxis*` conversions currently live in `XmiBeam`/`XmiColumn.from_dict`. If other languages emit arrays instead of strings, consider extending serializers so the mapping table remains valid for future integrations.
