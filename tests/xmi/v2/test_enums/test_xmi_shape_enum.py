from xmi.v2.models.enums.xmi_shape_enum import XmiShapeEnum

def test_xmi_shape_enum_values():
    assert XmiShapeEnum.RECTANGULAR.value == "Rectangular"
    assert XmiShapeEnum.CIRCULAR.value == "Circular"
    assert XmiShapeEnum.L_SHAPE.value == "L Shape"
    assert XmiShapeEnum.T_SHAPE.value == "T Shape"
    assert XmiShapeEnum.C_SHAPE.value == "C Shape"
    assert XmiShapeEnum.I_SHAPE.value == "I Shape"
    assert XmiShapeEnum.SQUARE_HOLLOW.value == "Square Hollow"
    assert XmiShapeEnum.RECTANGULAR_HOLLOW.value == "Rectangular Hollow"
    assert XmiShapeEnum.OTHERS.value == "Others"


# .venv/bin/python -m pytest tests/xmi/v2/test_enums/test_xmi_shape_enum.py