# `full_model_test_1.json` Ingestion Notes

The `tests/xmi/v2/test_inputs/full_model_test_1.json` payload was copied from an
older C# export. Running it through `XmiManager.read_xmi_dict()` highlights a
set of schema mismatches that prevent the Python parser from instantiating any
entities.

## What Happens Today
- Reading the file with the default `json.load()` fails because it starts with a
  UTF‑8 BOM. Opening the handle with `encoding="utf-8-sig"` fixes this.
- After decoding, the Python loader still returns `0` entities/relationships and
  no errors. The parser silently skips the payload because it expects the v2
  envelope keys (`Entities`, `Relationships`, `Histories`, `Errors`) and Pascal
  case field names (`ID`, `Name`, `EntityType`, etc.).

## Required JSON Shape (Python / Phase 6)
```json
{
  "Name": "Any descriptive title",
  "Entities": [{ "ID": "uuid", "Name": "", "EntityType": "XmiStructuralMaterial", ... }],
  "Relationships": [{ "ID": "rel-01", "Source": "entity-id", "Target": "entity-id", "EntityType": "XmiHasStructuralCurveMember" }],
  "Histories": [],
  "Errors": []
}
```

Each entity dictionary must use the aliases configured on the Pydantic models:
- `ID` (not `Id`)
- `Name`
- `Description`
- `EntityType`
- `IFCGUID` (all caps)
- `NativeId`
- `MaterialType`, `CurveMemberType`, etc.

Relationship dictionaries need `Source` / `Target` IDs plus `EntityType`.

## How to Update the C# Exporter (or preprocess the JSON)
1. **Rename the envelope keys** — emit `Entities`/`Relationships` instead of
   `nodes`/`edges`. Populate `Histories`/`Errors` even if they are empty arrays.
2. **Rename identifier fields** — map every `Id` property to `ID`. The Python
   aliases are case-sensitive, so `Id` is ignored. The same applies to
   `IfcGuid`, which must be `IFCGUID`.
3. **Preserve entity dictionaries as-is** — all other keys already match the
   expected PascalCase names, so once the aliases above are fixed the payload
   will deserialize without model changes.
4. **Export relationships** — the current file has an empty `edges` array. The
   Python library expects each edge to include `ID`, `Source`, `Target`,
   `EntityType`, and (optionally) metadata such as `Name` or `UmlType`.
5. **Strip the BOM** — update the C# writer to save UTF‑8 without BOM or run
   the JSON through a simple `payload = json.load(open(path, 'r', encoding='utf-8-sig'))`
   before handing it to `XmiManager`.

### Example Preprocessing Snippet
Until the C# exporter is updated, the JSON can be massaged locally:

```python
import json
from pathlib import Path

src = Path("tests/xmi/v2/test_inputs/full_model_test_1.json")
payload = json.loads(src.read_text(encoding="utf-8-sig"))

payload["Name"] = payload.get("Name") or "FullModelTest1"
payload["Entities"] = [
    {**node, "ID": node.pop("Id"), "IFCGUID": node.pop("IfcGuid", None)}
    for node in payload.pop("nodes", [])
]
payload["Relationships"] = [
    {**edge, "ID": edge.pop("Id")}
    for edge in payload.pop("edges", [])
]
payload.setdefault("Histories", [])
payload.setdefault("Errors", [])

Path("full_model_test_1_fixed.json").write_text(json.dumps(payload, indent=2))
```

Once the payload matches this structure, `XmiManager` ingests it cleanly and
any parsing errors will show up in `model.errors`. This document should let the
C# implementation team align their exporter with the Python schema.
