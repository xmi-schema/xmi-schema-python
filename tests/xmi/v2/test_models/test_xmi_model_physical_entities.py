"""Integration tests for Phase 4 entity mapping updates."""

import pytest

from tests.xmi.v2.test_inputs.xmi_model_physical_input import physical_model_data
from xmi.v2.models.xmi_model.xmi_model import XmiModel
from xmi.v2.models.entities.xmi_beam import XmiBeam
from xmi.v2.models.entities.xmi_column import XmiColumn
from xmi.v2.models.entities.xmi_slab import XmiSlab
from xmi.v2.models.entities.xmi_wall import XmiWall
from xmi.v2.models.entities.xmi_structural_curve_member import XmiStructuralCurveMember
from xmi.v2.models.relationships.xmi_has_structural_curve_member import XmiHasStructuralCurveMember


def test_xmi_model_loads_physical_entities_and_relationships():
    """Ensure the physical entities and bridge relationships load via mappings."""
    model = XmiModel()
    model.load_from_dict(physical_model_data)

    assert model.name == "PhysicalModel"
    assert not model.errors

    beams = [e for e in model.entities if isinstance(e, XmiBeam)]
    columns = [e for e in model.entities if isinstance(e, XmiColumn)]
    slabs = [e for e in model.entities if isinstance(e, XmiSlab)]
    walls = [e for e in model.entities if isinstance(e, XmiWall)]
    curves = [e for e in model.entities if isinstance(e, XmiStructuralCurveMember)]

    assert len(beams) == 1
    assert beams[0].entity_type == "XmiBeam"
    assert len(columns) == 1
    assert len(slabs) == 1
    assert len(walls) == 1
    assert len(curves) == 2

    rels = [r for r in model.relationships if isinstance(r, XmiHasStructuralCurveMember)]
    assert len(rels) == 2
    assert {rel.source.id for rel in rels} == {"beam-001", "column-001"}
    assert {rel.target.id for rel in rels} == {"curve-001", "curve-002"}


if __name__ == "__main__":
    pytest.main([__file__])
