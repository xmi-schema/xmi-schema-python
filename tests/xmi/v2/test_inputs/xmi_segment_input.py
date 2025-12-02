from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum

valid_segment_input = {
    "id": "eebf4b4f-14b0-4be1-8a6d-94b9858cff4a",
    "name": "Segment 1",
    "position": 1,
    "segment_type": XmiSegmentTypeEnum.LINE,
}

missing_position_input = {
    **valid_segment_input,
}
missing_position_input.pop("position")

invalid_segment_type_input = {
    **valid_segment_input,
    "segment_type": "INVALID_ENUM"
}