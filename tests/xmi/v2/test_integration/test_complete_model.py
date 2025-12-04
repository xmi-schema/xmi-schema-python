"""End-to-end tests for Phase 6 complete model scenarios."""

from __future__ import annotations

import json
from pathlib import Path

from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
from xmi.v2.models.entities.physical.xmi_column import XmiColumn
from xmi.v2.models.entities.physical.xmi_slab import XmiSlab
from xmi.v2.models.entities.physical.xmi_wall import XmiWall
from xmi.v2.models.entities.xmi_cross_section import XmiCrossSection
from xmi.v2.models.entities.xmi_material import XmiStructuralMaterial
from xmi.v2.models.entities.structural_analytical.xmi_structural_point_connection import XmiStructuralPointConnection
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_cross_section import XmiHasCrossSection
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from xmi.v2.models.xmi_model.xmi_model import XmiModel


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "test_inputs"


def load_complete_model() -> dict:
    with (FIXTURE_DIR / "complete_physical_model.json").open("r", encoding="utf-8") as fp:
        return json.load(fp)


def test_complete_model_entities_and_relationships_load():
    model = XmiModel()
    model.load_from_dict(load_complete_model())

    assert model.name == "CompletePhysicalModel"
    assert not model.errors

    materials = [e for e in model.entities if isinstance(e, XmiStructuralMaterial)]
    cross_sections = [e for e in model.entities if isinstance(e, XmiCrossSection)]
    beams = [e for e in model.entities if isinstance(e, XmiBeam)]
    columns = [e for e in model.entities if isinstance(e, XmiColumn)]
    slabs = [e for e in model.entities if isinstance(e, XmiSlab)]
    walls = [e for e in model.entities if isinstance(e, XmiWall)]
    points = [e for e in model.entities if isinstance(e, XmiStructuralPointConnection)]
    curves = [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]

    assert len(materials) == 1
    assert len(cross_sections) == 1
    assert len(beams) == 1
    assert len(columns) == 1
    assert len(slabs) == 1
    assert len(walls) == 1
    assert len(points) == 2
    assert len(curves) == 2

    bridge_relationships = [r for r in model.relationships if isinstance(r, XmiHasStructuralCurveMember)]
    assert len(bridge_relationships) == 2
    assert {rel.source.id for rel in bridge_relationships} == {"beam-complete", "column-complete"}

    cross_section_links = [r for r in model.relationships if isinstance(r, XmiHasCrossSection)]
    assert len(cross_section_links) == 2
    assert all(rel.target is cross_sections[0] for rel in cross_section_links)

    material_links = [r for r in model.relationships if isinstance(r, XmiHasStructuralMaterial)]
    assert len(material_links) == 1
    assert material_links[0].source is cross_sections[0]
    assert material_links[0].target is materials[0]


def test_complete_model_round_trip_exports_entities_with_aliases():
    model = XmiModel()
    source_data = load_complete_model()
    model.load_from_dict(source_data)

    round_trip = model.model_dump(by_alias=True, exclude_none=True)

    assert round_trip["Name"] == source_data["Name"]
    assert len(round_trip["Entities"]) == len(source_data["Entities"])
    assert len(round_trip["Relationships"]) == len(source_data["Relationships"])
