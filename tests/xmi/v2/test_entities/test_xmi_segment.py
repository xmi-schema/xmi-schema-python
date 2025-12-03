import pytest
from xmi.v2.models.entities.xmi_segment import XmiSegment
from tests.xmi.v2.test_inputs import xmi_segment_input as input_data

def test_valid_segment_instantiation():
    segment = XmiSegment(**input_data.valid_segment_input)

    assert segment.name == "Segment 1"
    assert segment.position == 1
    assert segment.segment_type.name == "LINE"
    assert segment.entity_type == "XmiSegment"


def test_missing_position_raises():
    with pytest.raises(ValueError) as exc_info:
        XmiSegment(**input_data.missing_position_input)

    assert "Position" in str(exc_info.value)


def test_invalid_segment_type_raises():
    with pytest.raises(ValueError) as exc_info:
        XmiSegment(**input_data.invalid_segment_type_input)

    assert "Input should be" in str(exc_info.value)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_segment.py