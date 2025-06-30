import pytest
from src.xmi.v2.models.entities.xmi_structural_storey import XmiStructuralStorey
from tests.xmi.v2.test_inputs import xmi_structural_storey_input as input_data


def test_valid_storey_instantiation():
    storey = XmiStructuralStorey(**input_data.valid_storey_input)

    assert storey.name == "Level 3"
    assert storey.native_id == "351314"
    assert storey.storey_elevation == 6000.0
    assert storey.storey_horizontal_reaction_x == "Fixed"
    assert storey.storey_vertical_reaction == "Roller"
    assert storey.entity_type == "XmiStructuralStorey"


def test_storey_instantiation_without_reactions():
    storey = XmiStructuralStorey(**input_data.valid_storey_missing_reactions_input)

    assert storey.name == "Level 3"
    assert storey.storey_horizontal_reaction_x is None
    assert storey.storey_horizontal_reaction_y is None
    assert storey.storey_vertical_reaction is None


def test_storey_inequality_different_native_id():
    storey_1 = XmiStructuralStorey(**input_data.valid_storey_input)
    storey_2 = XmiStructuralStorey(**{
        **input_data.valid_storey_input,
        "NativeId": "339"
    })

    assert storey_1 != storey_2


def test_storey_missing_required_fields_raises():
    with pytest.raises(ValueError) as exc_info:
        XmiStructuralStorey(**input_data.missing_field_input)
    
    assert "StoreyElevation" in str(exc_info.value)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_storey.py