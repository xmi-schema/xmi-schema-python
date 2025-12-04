"""Integration tests covering physical-to-analytical bridge behavior (Phase 6)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from xmi.v2.models.entities.physical.xmi_beam import XmiBeam
from xmi.v2.models.entities.physical.xmi_column import XmiColumn
from xmi.v2.models.entities.physical.xmi_slab import XmiSlab
from xmi.v2.models.entities.physical.xmi_wall import XmiWall
from xmi.v2.models.entities.structural_analytical.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember
from xmi.v2.models.xmi_model.xmi_model import XmiModel


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "test_inputs"


def load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open("r", encoding="utf-8") as fp:
        return json.load(fp)


def _load_model_from_fixture(name: str) -> XmiModel:
    model = XmiModel()
    model.load_from_dict(load_fixture(name))
    return model


def test_beam_bridge_relationship_is_created():
    model = _load_model_from_fixture("physical_beam_test.json")

    beams = [e for e in model.entities if isinstance(e, XmiBeam)]
    curves = [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]
    bridges = [r for r in model.relationships if isinstance(r, XmiHasStructuralCurveMember)]

    assert len(beams) == 1
    assert len(curves) == 1
    assert len(bridges) == 1
    assert bridges[0].source is beams[0]
    assert bridges[0].target is curves[0]


def test_column_bridge_relationship_is_created():
    model = _load_model_from_fixture("physical_column_test.json")

    columns = [e for e in model.entities if isinstance(e, XmiColumn)]
    curves = [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]
    bridges = [r for r in model.relationships if isinstance(r, XmiHasStructuralCurveMember)]

    assert len(columns) == 1
    assert len(curves) == 1
    assert len(bridges) == 1
    assert bridges[0].source is columns[0]
    assert bridges[0].target is curves[0]


@pytest.mark.parametrize(
    "fixture_file, entity_cls",
    [
        ("physical_slab_test.json", XmiSlab),
        ("physical_wall_test.json", XmiWall),
    ],
)
def test_slab_and_wall_have_no_bridge_relationships(fixture_file, entity_cls):
    model = _load_model_from_fixture(fixture_file)

    physical_entities = [e for e in model.entities if isinstance(e, entity_cls)]
    bridges = [r for r in model.relationships if isinstance(r, XmiHasStructuralCurveMember)]

    assert len(physical_entities) == 1
    assert not bridges


def test_invalid_bridge_relationship_logs_error():
    invalid_data = load_fixture("physical_beam_test.json")
    invalid_data["Relationships"].append(
        {
            "ID": "rel-invalid",
            "Source": "beam-bridge-001",
            "Target": "missing-curve",
            "EntityType": "XmiHasStructuralCurveMember",
            "Name": "InvalidBridge",
        }
    )

    model = XmiModel()
    model.load_from_dict(invalid_data)

    assert any(
        error.entity_type == "XmiHasStructuralCurveMember"
        and "Missing source or target" in error.message
        for error in model.errors
    )
