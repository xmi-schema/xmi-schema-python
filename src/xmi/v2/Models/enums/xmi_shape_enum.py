from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiShapeEnum(XmiBaseEnum):
    RECTANGULAR = "Rectangular"
    CIRCULAR = "Circular"
    L_SHAPE = "L Shape"
    T_SHAPE = "T Shape"
    C_SHAPE = "C Shape"
    I_SHAPE = "I Shape"
    SQUARE_HOLLOW = "Square Hollow"
    RECTANGULAR_HOLLOW = "Rectangular Hollow"
    OTHERS = "Others"