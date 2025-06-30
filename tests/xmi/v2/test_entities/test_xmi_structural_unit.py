import pytest
from uuid import UUID
from src.xmi.v2.models.entities.xmi_structural_unit import XmiStructuralUnit
from tests.xmi.v2.test_inputs import xmi_structural_unit_input as input_data


def test_valid_structural_unit():
    instance = XmiStructuralUnit(**input_data.valid_structural_unit_input)

    assert instance is not None
    assert instance.entity == "Beam"
    assert instance.attribute == "Length"
    assert instance.unit.value == "m"
    assert instance.entity_type == "XmiStructuralUnit"
    assert UUID(instance.id)
    assert instance.name.startswith("XmiStructuralUnit_")


def test_missing_entity():
    with pytest.raises(ValueError) as exc_info:
        XmiStructuralUnit(**input_data.missing_entity_input)
    assert "Entity" in str(exc_info.value)


def test_invalid_unit():
    with pytest.raises(ValueError) as exc_info:
        XmiStructuralUnit(**input_data.invalid_unit_input)
    assert "Input should be" in str(exc_info.value)

def test_explicit_id_and_name():
    instance = XmiStructuralUnit(**input_data.explicit_id_and_name_input)

    assert instance.id == "123e4567-e89b-12d3-a456-426614174000"
    assert instance.name == "CustomName"
    assert instance.entity == "Column"
    assert instance.unit.value == "mm"

# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_unit.py