# Optional, for forward declarations in Python 3.7+
from __future__ import annotations

from ..constants import *
from ..shapes.xmi_shape import *
from ..enums.xmi_shape_enums import XmiShapeEnum
from ..xmi_errors import *
from ..xmi_base import XmiBaseEntity
from .xmi_structural_material import XmiStructuralMaterial

from ..xmi_utilities import is_empty_or_whitespace

"""
1. Need to standardize "Parameters" property

"""

SHAPE_MAPPING = {
    XmiShapeEnum.RECTANGULAR: XmiShapeRectangle,
    XmiShapeEnum.CIRCULAR: XmiShapeCircle,
    XmiShapeEnum.L_SHAPE: XmiShapeL,
    XmiShapeEnum.T_SHAPE: XmiShapeT,
    XmiShapeEnum.C_SHAPE: XmiShapeC,
    XmiShapeEnum.I_SHAPE: XmiShapeI,
    XmiShapeEnum.SQUARE_HOLLOW: XmiShapeSquareHollow,
    XmiShapeEnum.RECTANGULAR_HOLLOW: XmiShapeRectangularHollow,
    XmiShapeEnum.OTHERS: XmiShapeOthers
}


class XmiCrossSection(XmiBaseEntity):
    __slots__ = XmiBaseEntity.__slots__ + ('_material',
                                           '_shape',
                                           '_parameters',
                                           '_area',
                                           '_second_moment_of_area_x_axis',
                                           '_second_moment_of_area_y_axis',
                                           "_radius_of_gyration_x_axis",
                                           "_radius_of_gyration_y_axis",
                                           "_elastic_modulus_x_axis",
                                           "_elastic_modulus_y_axis",
                                           "_plastic_modulus_x_axis",
                                           "_plastic_modulus_y_axis",
                                           "_torsional_constant")

    _attributes_needed = [slot[1:] if slot.startswith(
        '_') else slot for slot in __slots__ if slot != "_entity_type"]

    def __init__(self,
                 material: XmiStructuralMaterial,
                 shape: XmiShapeEnum,
                 parameters: list | tuple,
                 area: float | int | None = None,
                 second_moment_of_area_x_axis: float | int | None = None,
                 second_moment_of_area_y_axis: float | int | None = None,
                 radius_of_gyration_x_axis: float | int | None = None,
                 radius_of_gyration_y_axis: float | int | None = None,
                 elastic_modulus_x_axis: float | int | None = None,
                 elastic_modulus_y_axis: float | int | None = None,
                 plastic_modulus_x_axis: float | int | None = None,
                 plastic_modulus_y_axis: float | int | None = None,
                 torsional_constant: float | int | None = None,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 ifcguid: str = None,
                 **kwargs
                 ):
        entity_type = "XmiCrossSection"

        # Ensure material_type is provided
        if material is None:
            raise ValueError(
                "The 'material' parameter is compulsory and must be provided.")

        # Ensure material_type is provided
        if shape is None:
            raise ValueError(
                "The 'shape' parameter is compulsory and must be provided.")

        # Ensure material_type is provided
        if parameters is None:
            raise ValueError(
                "The 'parameters' parameter is compulsory and must be provided.")

        # Initialize parent class
        super().__init__(id=id,
                         name=name,
                         ifcguid=ifcguid,
                         description=description,
                         entity_type=entity_type
                         )

        # Initialize attributes
        self.set_attributes(
            material=material,
            shape=shape,
            parameters=parameters,
            second_moment_of_area_x_axis=second_moment_of_area_x_axis,
            second_moment_of_area_y_axis=second_moment_of_area_y_axis,
            radius_of_gyration_x_axis=radius_of_gyration_x_axis,
            radius_of_gyration_y_axis=radius_of_gyration_y_axis,
            elastic_modulus_x_axis=elastic_modulus_x_axis,
            elastic_modulus_y_axis=elastic_modulus_y_axis,
            plastic_modulus_x_axis=plastic_modulus_x_axis,
            plastic_modulus_y_axis=plastic_modulus_y_axis,
            torsional_constant=torsional_constant,
            area=area,
            **kwargs)

    def set_attributes(self,
                       material: XmiStructuralMaterial,
                       shape: XmiShapeEnum,
                       parameters: list[float | int] | tuple[float | int],
                       second_moment_of_area_x_axis: float | int | None,
                       second_moment_of_area_y_axis: float | int | None,
                       radius_of_gyration_x_axis: float | int | None,
                       radius_of_gyration_y_axis: float | int | None,
                       elastic_modulus_x_axis: float | int | None,
                       elastic_modulus_y_axis: float | int | None,
                       plastic_modulus_x_axis: float | int | None,
                       plastic_modulus_y_axis: float | int | None,
                       torsional_constant: float | int | None,
                       area: float | int,
                       **kwargs):
        attributes = [
            ('material', material),
            ('shape', shape),
            ('parameters', parameters),
            ('area', area),
            ('second_moment_of_area_x_axis', second_moment_of_area_x_axis),
            ('second_moment_of_area_y_axis', second_moment_of_area_y_axis),
            ('radius_of_gyration_x_axis', radius_of_gyration_x_axis),
            ('radius_of_gyration_y_axis', radius_of_gyration_y_axis),
            ('elastic_modulus_x_axis', elastic_modulus_x_axis),
            ('elastic_modulus_y_axis', elastic_modulus_y_axis),
            ('plastic_modulus_x_axis', plastic_modulus_x_axis),
            ('plastic_modulus_y_axis', plastic_modulus_y_axis),
            ('torsional_constant', torsional_constant)
        ]

        for attr_name, attr_value in attributes:
            value = kwargs.get(attr_name, attr_value)
            try:
                setattr(self, attr_name, value)
            except AttributeError as e:
                print(
                    f"Caught an AttributeError while setting {attr_name}: {e}")
                setattr(self, attr_name, None)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, XmiStructuralMaterial):
            raise TypeError(
                "Material should be an XmiStructuralMaterial")
        self._material = value

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        if not isinstance(value, XmiShapeEnum):
            raise TypeError(
                "Shape should be of type XmiShapeEnum")
        self._shape = value

    # Similarly, for other properties:

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        # check if the datatype is correct
        if not isinstance(value, (list, tuple)):
            raise TypeError(
                "Parameters should be of type list or tuple")

        # check for quantity of params
        if self.shape and self.shape != XmiShapeEnum.OTHERS and value:
            mapped_class = SHAPE_MAPPING[self.shape]
            mapped_class_instance: XmiShape = mapped_class()
            param_required_length = mapped_class_instance.parameter_quantity
            value_length = len(value)
            if value_length != param_required_length:
                raise XmiInconsistentDataTypeError(
                    f"The parameter length is different than required XmiShape's parameter_quantity value")
        # check for every item within the list of tuple to be an int or float value and all data needs to be at least 0.0
        for item in value:
            if not isinstance(item, (int, float)):
                raise ValueError(
                    f"All items must be instances of float or int, got {type(item)} instead.")
            if item < 0.0:
                raise ValueError(
                    f"Value cannot be smaller than 0"
                )
        self._parameters = tuple(value)

    # to be considered optional as of now
    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError("Area should be of type float,int or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Area should be larger than 0.0")
        self._area = value

    @property
    def second_moment_of_area_x_axis(self):
        return self._second_moment_of_area_x_axis

    @second_moment_of_area_x_axis.setter
    def second_moment_of_area_x_axis(self, value):
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError(
                "Ix (Second Moment of Area - x axis) should be of type float,int or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Ix should be larger than 0.0")
        self._second_moment_of_area_x_axis = value

    @property
    def second_moment_of_area_y_axis(self):
        return self._second_moment_of_area_y_axis

    @second_moment_of_area_y_axis.setter
    def second_moment_of_area_y_axis(self, value):
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError(
                "Iy (Second Moment of Area - y axis) should be of type float,int or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Iy should be larger than 0.0")
        self._second_moment_of_area_y_axis = value

    @property
    def radius_of_gyration_x_axis(self):
        return self._radius_of_gyration_x_axis

    @radius_of_gyration_x_axis.setter
    def radius_of_gyration_x_axis(self, value):
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError(
                "rx (Radius of Gyration - x axis) should be of type float or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("rx should be larger than 0.0")
        self._radius_of_gyration_x_axis = value

    @property
    def radius_of_gyration_y_axis(self):
        return self._radius_of_gyration_y_axis

    @radius_of_gyration_y_axis.setter
    def radius_of_gyration_y_axis(self, value):
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError(
                "ry (Radius of Gyration - y axis) should be of type float or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("ry should be larger than 0.0")
        self._radius_of_gyration_y_axis = value

    @property
    def elastic_modulus_x_axis(self):
        return self._elastic_modulus_x_axis

    @elastic_modulus_x_axis.setter
    def elastic_modulus_x_axis(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(
                "Ex (E Modulus - x axis) should be of type float, integer, or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Ex should be larger than 0.0")
        self._elastic_modulus_x_axis = value

    @property
    def elastic_modulus_y_axis(self):
        return self._elastic_modulus_y_axis

    @elastic_modulus_y_axis.setter
    def elastic_modulus_y_axis(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(
                "Ey (E Modulus - y axis) should be of type float, integer, or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Ey should be larger than 0.0")
        self._elastic_modulus_y_axis = value

    @property
    def torsional_constant(self):
        return self._torsional_constant

    @torsional_constant.setter
    def torsional_constant(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(
                "Torsional Constant should be of type float, integer, or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError("Torsional Constant should be larger than 0.0")
        self._torsional_constant = value

    @property
    def plastic_modulus_x_axis(self):
        return self._plastic_modulus_x_axis

    @plastic_modulus_x_axis.setter
    def plastic_modulus_x_axis(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(
                "Zx (Plastic Modulus - x axis) should be of type float, integer, or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError(
        #         "Zx (Plastic Modulus - x axis) should be larger than 0.0")
        self._plastic_modulus_x_axis = value

    @property
    def plastic_modulus_y_axis(self):
        return self._plastic_modulus_y_axis

    @plastic_modulus_y_axis.setter
    def plastic_modulus_y_axis(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(
                "Zy (Plastic Modulus - y axis) should be of type float, integer, or None")
        # if value is not None and value <= 0.0:
        #     raise ValueError(
        #         "Zy (Plastic Modulus - y axis) should be larger than 0.0")
        self._plastic_modulus_y_axis = value

    # def is_empty_or_whitespace(input_string: str) -> bool:
    #     return not input_string or not input_string.strip()

    @classmethod
    def convert_parameter_string_to_tuple(self, parameter_str: str) -> tuple[int, float]:
        parameter_list: list[str] = parameter_str.split(';')
        for param in parameter_list:
            if is_empty_or_whitespace(param):
                raise XmiInconsistentDataTypeError(
                    f"The individual parameter [{param}] within the XmiCrossSection 'parameters' attribute should not be empty string or empty space")
            try:
                float_value = float(param)
            except ValueError:
                raise XmiInconsistentDataTypeError(
                    f"The parameter [{param}] within the XmiCrossSection 'parameters' attribute should be convertible to float")

        parameter_tuple = tuple([float(param) for param in parameter_list])

        return parameter_tuple

    # from_dict class method is used to do data conversion
    @classmethod
    def from_dict(cls, obj: dict) -> XmiCrossSection:
        instance: XmiCrossSection | None = None
        error_logs = []
        processed_data = obj.copy()

        for attr in cls._attributes_needed:
            if attr not in processed_data:
                error_logs.append(Exception(f"Missing attribute: {attr}"))
                processed_data[attr] = None

        # for type conversion when reading dictionary
        try:
            # check for material found
            material_found: XmiStructuralMaterial | str | None = processed_data['material']
            if material_found is None:
                error_logs.append(XmiMissingReferenceInstanceError(
                    "Please provide material value of type XmiStructuralMaterial"))
                return None, error_logs
            else:
                if not isinstance(material_found, XmiStructuralMaterial):
                    error_logs.append(XmiInconsistentDataTypeError(
                        "material provided need to be of instance XmiStructuralMaterial"))

            # check for conversion of parameters to tuple of parameters suitable for the Shape
            shape_found: XmiShapeEnum | None | str = processed_data['shape']
            if shape_found is None:
                error_logs.append(XmiMissingRequiredAttributeError(
                    "Please provide value of type XmiShapeEnum for the shape attribute"))
                return None, error_logs
            else:
                shape_found = XmiShapeEnum.from_attribute_get_enum(
                    processed_data['shape'])
                if not isinstance(shape_found, XmiShapeEnum):
                    error_logs.append(XmiInconsistentDataTypeError(
                        "shape value provided need to be of instance XmiShapeEnum"))
                    return None, error_logs
                processed_data['shape'] = shape_found

            # check for params
            parameters_found = processed_data['parameters']
            if parameters_found is None:
                error_logs.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the parameters attribute"))
                return None, error_logs
            else:
                parameters_found: tuple[float | int] = XmiCrossSection.convert_parameter_string_to_tuple(
                    processed_data['parameters'])

                if not isinstance(parameters_found, tuple):
                    error_logs.append(XmiInconsistentDataTypeError(
                        "parameters value after conversion using the convert_parameter_string_to_tuple function should be of type tuple"))
                    return None, error_logs
                processed_data['parameters'] = parameters_found
        except KeyError as e:
            error_logs.append(e)
            return None, error_logs

        # del processed_data['material']

        try:
            instance = cls(
                # material=material_found,
                **processed_data)
        except Exception as e:
            error_logs.append(
                Exception(f"Error instantiating XmiCrossSection: {obj}"))

        return instance, error_logs

    # additional parameters are used to inject reference elements
    @classmethod
    def from_xmi_dict_obj(cls, xmi_dict_obj: dict,
                          material: XmiStructuralMaterial = None) -> XmiCrossSection:
        # Define a mapping from snake_case keys to custom keys
        KEY_MAPPING = {
            "Name": "name",
            "Material": "material",
            "Parameters": "parameters",
            "Shape": "shape",
            "Ix": "second_moment_of_area_x_axis",
            "Iy": "second_moment_of_area_y_axis",
            "rx": "radius_of_gyration_x_axis",
            "ry": "radius_of_gyration_y_axis",
            "Ex": "elastic_modulus_x_axis",
            "Ey": "elastic_modulus_y_axis",
            "Zx": "plastic_modulus_x_axis",
            "Zy": "plastic_modulus_y_axis",
            "J": "torsional_constant",
            "Area": "area",
            "Description": "description",
            "ID": "id",
            "IFCGUID": "ifcguid",
        }

        instance: XmiCrossSection | None = None
        error_logs: list[Exception] = []
        processed_data: dict = {KEY_MAPPING.get(
            key, key): value for key, value in xmi_dict_obj.items()}

        if 'material' in processed_data.keys() and material is not None:
            processed_data['material'] = material

        instance, error_logs_found = cls.from_dict(
            processed_data)

        error_logs.extend(error_logs_found)

        return instance, error_logs
