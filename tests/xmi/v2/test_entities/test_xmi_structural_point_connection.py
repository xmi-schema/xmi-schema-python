import pytest
from xmi.v2.models.entities.xmi_structural_point_connection import XmiStructuralPointConnection
from tests.xmi.v2.test_inputs import xmi_structural_point_connection_input as input_data


def test_valid_point_connection_from_dict():
    instance, errors = XmiStructuralPointConnection.from_dict(input_data.valid_point_connection_input)

    assert instance is not None
    assert instance.name == "Point Connection 1"
    assert instance.point.x == -6067.8
    assert instance.point.y == -7812.7
    assert instance.point.z == -3667.1
    assert instance.entity_type == "XmiStructuralPointConnection"
    assert errors == []


def test_missing_required_fields_from_dict():
    instance, errors = XmiStructuralPointConnection.from_dict(input_data.missing_required_fields_input)

    assert instance is None
    assert len(errors) > 0
    assert any("Missing attribute: name" in str(e) for e in errors)
    assert any("Missing attribute: point" in str(e) for e in errors)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_point_connection.py