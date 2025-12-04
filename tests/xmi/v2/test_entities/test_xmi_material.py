from xmi.v2.models.entities.xmi_material import XmiMaterial
from tests.xmi.v2.test_inputs import xmi_structural_material_input as input_data


def test_valid_material():
    instance, errors = XmiMaterial.from_dict(input_data.valid_material_input)
    assert instance is not None
    assert instance.material_type.value == "Concrete"
    assert instance.grade == 35.0
    assert not errors


def test_missing_material_type():
    instance, errors = XmiMaterial.from_dict(input_data.missing_material_type_input)
    assert instance is None
    assert any("material_type" in str(e) for e in errors)


def test_invalid_material_type():
    instance, errors = XmiMaterial.from_dict(input_data.invalid_material_type_input)
    assert instance is None
    assert any("material_type" in str(e) for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_material.py