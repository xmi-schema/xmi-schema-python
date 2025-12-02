from xmi.v2.models.entities.xmi_structural_cross_section import XmiStructuralCrossSection
from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum
from tests.xmi.v2.test_inputs.xmi_structural_cross_section_input import valid_cross_section_input

def test_cross_section_without_material():
    instance, errors = XmiStructuralCrossSection.from_dict(valid_cross_section_input)

    assert not errors, f"Unexpected validation errors: {errors}"
    assert instance is not None
    assert instance.name == "300 x 300mm"
    assert instance.shape == XmiShapeEnum.UNKNOWN
    assert instance.parameters == (300.0, 300.0)


# .venv/bin/python -m pytest tests/xmi/v2/test_entities/test_xmi_structural_cross_section.py