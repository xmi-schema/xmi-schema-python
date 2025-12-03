# Optional, for forward declarations in Python 3.7+
from __future__ import annotations

from ..entities.xmi_segment import XmiSegment
from ..entities.xmi_structural_cross_section import XmiCrossSection

from .xmi_structural_point_connection import XmiStructuralPointConnection
from ..xmi_base import XmiBaseEntity
from ..enums.xmi_structural_curve_member_enums import *
from ..geometries.xmi_base_geometry import XmiBaseGeometry

from ..xmi_errors import *


class XmiStructuralCurveMember(XmiBaseEntity):
    __slots__ = XmiBaseEntity.__slots__ + \
        ('_cross_section',
         '_storey',
         '_curve_member_type',
         '_nodes',
         '_segments',
         '_system_line',
         '_begin_node',
         '_end_node',
         '_length',
         '_local_axis_x',
         '_local_axis_y',
         '_local_axis_z',
         '_begin_node_x_offset',
         '_end_node_x_offset',
         '_begin_node_y_offset',
         '_end_node_y_offset',
         '_begin_node_z_offset',
         '_end_node_z_offset',
         '_end_fixity_start',
         '_end_fixity_end',
         )

    _attributes_needed = [slot[1:] if slot.startswith(
        '_') else slot for slot in __slots__ if slot != "_entity_type"]

    def __init__(self,
                 cross_section: XmiCrossSection,
                 curve_member_type: XmiStructuralCurveMemberTypeEnum,
                 system_line: XmiStructuralCurveMemberSystemLineEnum,
                 local_axis_x: tuple = (1.0, 0.0, 0.0),
                 local_axis_y: tuple = (0.0, 1.0, 0.0),
                 local_axis_z: tuple = (0.0, 0.0, 1.0),
                 begin_node_x_offset: float | int = 0.0,
                 end_node_x_offset: float | int = 0.0,
                 begin_node_y_offset: float | int = 0.0,
                 end_node_y_offset: float | int = 0.0,
                 begin_node_z_offset: float | int = 0.0,
                 end_node_z_offset: float | int = 0.0,
                 segments: list[XmiBaseGeometry] = [],
                 nodes: list[XmiStructuralPointConnection] = [],
                 length: int | float | None = None,
                 begin_node: XmiStructuralPointConnection = None,
                 end_node: XmiStructuralPointConnection = None,
                 #  end_fixity_start,  # optional
                 #  end_fixity_end,  # optional
                 storey: str | None = None,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 ifcguid: str = None,
                 **kwargs
                 ):
        entity_type = "XmiStructuralCurveMember"

        # Check for mutual exclusivity, things that are optional should be inside any
        # if kwargs and any([
        #         length,
        #         storey,
        #         id, name, description, ifcguid
        # ]):
        #     raise ValueError(
        #         "Please use either standard parameters or kwargs, not both.")

        # Ensure cross_section is provided
        if cross_section is None:
            raise ValueError(
                "The 'cross_section' parameter is compulsory and must be provided.")

        # Ensure curve_member_type is provided
        if curve_member_type is None:
            raise ValueError(
                "The 'curve_member_type' parameter is compulsory and must be provided.")

        # Ensure system_line is provided
        if system_line is None:
            raise ValueError(
                "The 'system_line' parameter is compulsory and must be provided.")

        # Ensure nodes is provided
        if nodes is None:
            raise ValueError(
                "The 'nodes' parameter is compulsory and must be provided.")

        # Ensure segments is provided
        if segments is None:
            # if segments is None and not in kwargs, then check if the nodes and segment_types is provided
            # if not provided then only raise error
            raise ValueError(
                "The 'segments' parameter is compulsory and must be provided.")

        # Ensure begin_node is provided
        if begin_node is None:
            raise ValueError(
                "The 'begin_node' parameter is compulsory and must be provided.")

        # Ensure end_node is provided
        if end_node is None:
            raise ValueError(
                "The 'end_node' parameter is compulsory and must be provided.")

        # Initialize parent class
        super().__init__(id=id,
                         name=name,
                         ifcguid=ifcguid,
                         description=description,
                         entity_type=entity_type
                         )

        # Initialize attributes
        self.set_attributes(
            cross_section=cross_section,
            curve_member_type=curve_member_type,
            nodes=nodes,
            segments=segments,
            system_line=system_line,
            begin_node=begin_node,
            end_node=end_node,
            local_axis_x=local_axis_x,
            local_axis_y=local_axis_y,
            local_axis_z=local_axis_z,
            begin_node_x_offset=begin_node_x_offset,
            end_node_x_offset=end_node_x_offset,
            begin_node_y_offset=begin_node_y_offset,
            end_node_y_offset=end_node_y_offset,
            begin_node_z_offset=begin_node_z_offset,
            end_node_z_offset=end_node_z_offset,
            length=length,
            storey=storey,
            # segment_types=segment_types,
            ** kwargs)

    def set_attributes(self,
                       cross_section: XmiCrossSection,
                       curve_member_type: XmiStructuralCurveMemberTypeEnum,
                       system_line: XmiStructuralCurveMemberSystemLineEnum,
                       nodes: list[XmiStructuralPointConnection],
                       segments: list[XmiSegment],
                       #    segment_types: list[XmiSegmentTypeEnum],
                       begin_node: XmiStructuralPointConnection,
                       end_node: XmiStructuralPointConnection,
                       local_axis_x,
                       local_axis_y,
                       local_axis_z,
                       begin_node_x_offset,
                       end_node_x_offset,
                       begin_node_y_offset,
                       end_node_y_offset,
                       begin_node_z_offset,
                       end_node_z_offset,
                       length,
                       storey,
                       **kwargs):

        attributes = [
            ('cross_section', cross_section),
            ('curve_member_type', curve_member_type),
            ('nodes', nodes),
            ('segments', segments),
            ('system_line', system_line),
            ('begin_node', begin_node),
            ('end_node', end_node),
            ('local_axis_x', local_axis_x),
            ('local_axis_y', local_axis_y),
            ('local_axis_z', local_axis_z),
            ('begin_node_x_offset', begin_node_x_offset),
            ('end_node_x_offset', end_node_x_offset),
            ('begin_node_y_offset', begin_node_y_offset),
            ('end_node_y_offset', end_node_y_offset),
            ('begin_node_z_offset', begin_node_z_offset),
            ('end_node_z_offset', end_node_z_offset),
            ('length', length),
            ('storey', storey)
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
    def storey(self):
        return self._storey

    @storey.setter
    def storey(self, value):
        if not isinstance(value, str):
            raise TypeError("storey attribute should be an str")
        self._storey = value

    @property
    def curve_member_type(self):
        return self._curve_member_type

    @curve_member_type.setter
    def curve_member_type(self, value):
        if not isinstance(value, (XmiStructuralCurveMemberTypeEnum)):
            raise TypeError(
                "curve_member_type should be type XmiStructuralCurveMemberTypeEnum")
        self._curve_member_type = value

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        if not isinstance(value, list):
            raise TypeError("nodes attribute should be a list")
        for item in value:
            if not isinstance(item, XmiStructuralPointConnection):
                raise ValueError(
                    f"All items must be instances of XmiStructuralPointConnection, got {type(item)} instead.")
        self._nodes = value

    @property
    def begin_node(self):
        return self._begin_node

    @begin_node.setter
    def begin_node(self, value):
        if not isinstance(value, XmiStructuralPointConnection):
            raise TypeError(
                "begin_node should be of type XmiStructuralPointConnection")
        self._begin_node = value

    @property
    def end_node(self):
        return self._end_node

    @end_node.setter
    def end_node(self, value):
        if not isinstance(value, XmiStructuralPointConnection):
            raise TypeError(
                "EndNode should be of type XmiStructuralPointConnection")
        self._end_node = value

    @property
    def cross_section(self):
        return self._cross_section

    @cross_section.setter
    def cross_section(self, value):
        if not isinstance(value, XmiCrossSection):
            raise TypeError(
                "cross_section should be of type XmiCrossSection")
        self._cross_section = value

    @property
    def system_line(self):
        return self._system_line

    @system_line.setter
    def system_line(self, value):
        if not isinstance(value, XmiStructuralCurveMemberSystemLineEnum):
            raise TypeError(
                "system_line should be of type XmiStructuralCurveMemberSystemLineEnum")
        self._system_line = value

    @property
    def segments(self):
        return self._segments

    @segments.setter
    def segments(self, value):
        if not isinstance(value, list):
            raise TypeError(
                "Segments should be of type list")

        # if len(value) < 1:
        #     raise ValueError(
        #         "'segments' list should have at least 1 items of type XmiSegment")

        for item in value:
            if not isinstance(item, XmiSegment):
                raise ValueError(
                    f"All items must be instances of XmiSegment, got {type(item)} instead.")
        self._segments = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not isinstance(value, (int, float, None)):
            raise TypeError(
                "length should be of type float or integer")
        self._length = value

    @property
    def local_axis_x(self):
        return self._local_axis_x

    @local_axis_x.setter
    def local_axis_x(self, value):
        if not isinstance(value, tuple):
            raise TypeError(
                "local_axis_x should be type XmiStructuralCurveMemberTypeEnum")
        self._local_axis_x = value

    @property
    def local_axis_y(self):
        return self._local_axis_y

    @local_axis_y.setter
    def local_axis_y(self, value):
        if not isinstance(value, tuple):
            raise TypeError(
                "local_axis_y should be type XmiStructuralCurveMemberTypeEnum")
        self._local_axis_y = value

    @property
    def local_axis_z(self):
        return self._local_axis_z

    @local_axis_z.setter
    def local_axis_z(self, value):
        if not isinstance(value, tuple):
            raise TypeError(
                "local_axis_z should be type XmiStructuralCurveMemberTypeEnum")
        self._local_axis_z = value

    @property
    def begin_node_x_offset(self):
        return self._begin_node_x_offset

    @begin_node_x_offset.setter
    def begin_node_x_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "begin_node_x_offset should be of type float or int")
        self._begin_node_x_offset = value

    @property
    def begin_node_y_offset(self):
        return self._begin_node_y_offset

    @begin_node_y_offset.setter
    def begin_node_y_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "begin_node_y_offset should be of type float or int")
        self._begin_node_y_offset = value

    @property
    def begin_node_z_offset(self):
        return self._begin_node_z_offset

    @begin_node_z_offset.setter
    def begin_node_z_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "begin_node_z_offset should be of type float or int")
        self._begin_node_z_offset = value

    @property
    def end_node_x_offset(self):
        return self._end_node_x_offset

    @end_node_x_offset.setter
    def end_node_x_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "end_node_x_offset should be of type float or int")
        self._end_node_x_offset = value

    @property
    def end_node_y_offset(self):
        return self._end_node_y_offset

    @end_node_y_offset.setter
    def end_node_y_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "end_node_y_offset should be of type float or int")
        self._end_node_y_offset = value

    @property
    def end_node_z_offset(self):
        return self._end_node_z_offset

    @end_node_z_offset.setter
    def end_node_z_offset(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "end_node_z_offset should be of type float or int")
        self._end_node_z_offset = value

    @property
    def end_fixity_start(self):
        return self._end_fixity_start

    @end_fixity_start.setter
    def end_fixity_start(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "end_fixity_start should be of type float or int")
        self._end_fixity_start = value

    @property
    def end_fixity_end(self):
        return self._end_fixity_end

    @end_fixity_end.setter
    def end_fixity_end(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                "end_fixity_end should be of type float or int")
        self._end_fixity_end = value

    def is_empty_or_whitespace(input_string: str) -> bool:
        return not input_string or not input_string.strip()

    @classmethod
    def convert_local_axis_string_to_tuple(cls, axis_direction, local_axis_str: str) -> tuple:
        local_axis_list: list[str] = local_axis_str.split(',')
        if len(local_axis_list) != 3:
            raise XmiMissingRequiredAttributeError(
                f"The XmiStructuralCurveMember 'local_axis_{axis_direction}' attribute should have 3 parameters")

        for local_axis_value in local_axis_list:
            if cls.is_empty_or_whitespace(local_axis_value):
                raise XmiInconsistentDataTypeError(
                    f"The individual parameter [{local_axis_value}] within the XmiStructuralCurveMember 'local_axis_{axis_direction}' attribute should not be empty string or empty space")
            try:
                float_value = float(local_axis_value)
            except ValueError:
                raise XmiInconsistentDataTypeError(
                    f"The parameter [{local_axis_value}] within the XmiStructuralCurveMember 'local_axis_{axis_direction}' attribute should be convertible to float")

        parameter_tuple = tuple([float(param) for param in local_axis_list])
        return parameter_tuple

    @classmethod
    def from_dict(cls, obj: dict) -> XmiStructuralCurveMember:
        instance = None
        exceptions = []
        processed_data = obj.copy()

        for attr in cls._attributes_needed:
            if attr not in processed_data:
                exceptions.append(Exception(f"Missing attribute: {attr}"))
                processed_data[attr] = None

        # for type conversion when reading dictionary
        try:
            # check for cross_section_found
            cross_section_found = processed_data['cross_section']
            if cross_section_found is None:
                exceptions.append(XmiMissingReferenceInstanceError(
                    "Please provide cross_section value of type XmiCrossSection"))
                return None, exceptions
            if not isinstance(cross_section_found, XmiCrossSection):
                exceptions.append(XmiInconsistentDataTypeError(
                    "cross_section provided need to be of instance XmiCrossSection"))
                return None, exceptions

            # check for nodes
            nodes_found = processed_data['nodes']
            if nodes_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the nodes attribute"))
                return None, exceptions

            if not isinstance(nodes_found, list):
                exceptions.append(XmiInconsistentDataTypeError(
                    "nodes value provided need to be of instance list"))
                return None, exceptions
            for node in nodes_found:
                if not isinstance(node, XmiStructuralPointConnection):
                    exceptions.append(XmiInconsistentDataTypeError(
                        "nodes value provided need to be of instance XmiStructuralPointConnection"))
                    return None, exceptions

            # check for segments
            segments_found = processed_data['segments']
            if segments_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the segments attribute"))
                return None, exceptions

            # if segment is not type list, return error
            if not isinstance(segments_found, list):
                exceptions.append(XmiInconsistentDataTypeError(
                    "segments value provided need to be of instance list"))
                return None, exceptions

            # if segments length = 0, return error
            if len(segments_found) == 0:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "The 'segments' parameter requires at least 1 segment of Type XmiSegment"))
                return None, exceptions

            # check for all segment datatypes
            for segment in segments_found:
                if not isinstance(segment, XmiSegment):
                    exceptions.append(XmiInconsistentDataTypeError(
                        "segment value provided need to be of instance XmiSegment"))
                    return None, exceptions

            # setting up begin_node and end_node of element
            if len(segments_found) > 0:
                segment_begin: XmiSegment = segments_found[0]
                segment_end: XmiSegment = segments_found[len(
                    segments_found) - 1]

                begin_node_found = next(
                    (spc for spc in nodes_found if spc == segment_begin.begin_node), None)
                end_node_found = next(
                    (spc for spc in nodes_found if spc == segment_end.end_node), None)

                # check against xmi_dict provided
                if begin_node_found.name != processed_data['begin_node']:
                    exceptions.append(ValueError(
                        "'begin_node' in dictionary differs than the 1 defined in dictionary"))
                    return None, exceptions
                if end_node_found.name != processed_data['end_node']:
                    exceptions.append(ValueError(
                        "'end_node' in dictionary differs than the 1 defined in dictionary"))
                    return None, exceptions

                processed_data['begin_node'] = begin_node_found
                processed_data['end_node'] = end_node_found

            # check for local_axis_x
            local_axis_x_found = processed_data['local_axis_x']
            if local_axis_x_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the parameters attribute"))
                return None, exceptions

            local_axis_x_found = XmiStructuralCurveMember.convert_local_axis_string_to_tuple(
                'x', processed_data['local_axis_x'])

            if not isinstance(local_axis_x_found, tuple):
                exceptions.append(XmiInconsistentDataTypeError(
                    "local_axis_x value after conversion using the convert_parameter_string_to_tuple function should be of type tuple"))
                return None, exceptions
            processed_data['local_axis_x'] = local_axis_x_found

            # check for local_axis_y
            local_axis_y_found = processed_data['local_axis_y']
            if local_axis_y_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the parameters attribute"))
                return None, exceptions
            local_axis_y_found = XmiStructuralCurveMember.convert_local_axis_string_to_tuple(
                'y', processed_data['local_axis_y'])

            if not isinstance(local_axis_y_found, tuple):
                exceptions.append(XmiInconsistentDataTypeError(
                    "local_axis_y value after conversion using the convert_parameter_string_to_tuple function should be of type tuple"))
                return None, exceptions
            processed_data["local_axis_y"] = local_axis_y_found

            # check for local_axis_z
            local_axis_z_found = processed_data['local_axis_z']
            if local_axis_z_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the parameters attribute"))
                return None, exceptions
            local_axis_z_found = XmiStructuralCurveMember.convert_local_axis_string_to_tuple(
                'z', processed_data['local_axis_z'])
            if not isinstance(local_axis_z_found, tuple):
                exceptions.append(XmiInconsistentDataTypeError(
                    "local_axis_z value after conversion using the convert_parameter_string_to_tuple function should be of type tuple"))
                return None, exceptions
            processed_data["local_axis_z"] = local_axis_z_found

            # check system_line
            system_line_found = processed_data['system_line']
            if system_line_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the system_line attribute"))
                return None, exceptions
            system_line_found = XmiStructuralCurveMemberSystemLineEnum.from_attribute_get_enum(
                processed_data['system_line'])
            processed_data["system_line"] = system_line_found

            # check curve_member_type
            curve_member_type_found = processed_data['curve_member_type']
            if curve_member_type_found is None:
                exceptions.append(XmiMissingRequiredAttributeError(
                    "Please provide value for the curve_member_type attribute"))
                return None, exceptions
            curve_member_type_found = XmiStructuralCurveMemberTypeEnum.from_attribute_get_enum(
                processed_data['curve_member_type'])
            processed_data["curve_member_type"] = curve_member_type_found

        except KeyError as e:
            exceptions.append(e)
            return None, exceptions

        try:
            instance = cls(
                ** processed_data)
        except Exception as e:
            exceptions.append(
                Exception(f"Error instantiating XmiStructuralCurveMember: {obj}"))

        return instance, exceptions

    # additional parameters are used to inject reference elements
    @classmethod
    def from_xmi_dict_obj(cls, xmi_dict_obj: dict,
                          cross_section: XmiCrossSection = None,
                          nodes: list[XmiStructuralPointConnection] = None,
                          segments: list[XmiBaseEntity] = None,
                          ) -> XmiStructuralCurveMember:
        # Define a mapping from snake_case keys to custom keys
        KEY_MAPPING = {
            "CrossSection": "cross_section",
            "Storey": "storey",
            "Type": "curve_member_type",
            "Nodes": "nodes",
            "Segments": "segments",
            "SystemLine": "system_line",
            "BeginNode": "begin_node",
            "EndNode": "end_node",
            "Length": "length",
            "LocalAxisX": "local_axis_x",
            "LocalAxisY": "local_axis_y",
            "LocalAxisZ": "local_axis_z",
            "BeginNodeXOffset": "begin_node_x_offset",
            "EndNodeXOffset": "end_node_x_offset",
            "BeginNodeYOffset": "begin_node_y_offset",
            "EndNodeYOffset": "end_node_y_offset",
            "BeginNodeZOffset": "begin_node_z_offset",
            "EndNodeZOffset": "end_node_z_offset",
            "EndFixityStart": "end_fixity_start",
            "EndFixityEnd": "end_fixity_end",
            "Name": "name",
            "Description": "description",
            "ID": "id",
            "IFCGUID": "ifcguid",
            # "CircularArcCentre": "circular_arc_centre", # NOT IN USE
            # "CircularArcRadius": "circular_arc_radius", # NOT IN USE
            # "StiffnessModifierArea": "stiffness_modifier_area",
            # "StiffnessModifierAsy": "stiffness_modifier_shear_local_y_axis",
            # "StiffnessModifierAsz": "stiffness_modifier_shear_local_z_axis",
            # "StiffnessModifierTorsion": "stiffness_modifier_shear_torsion",
            # "StiffnessModifierIyy": "stiffness_modifier_moment_local_y_axis",
            # "StiffnessModifierIzz": "stiffness_modifier_moment_local_z_axis",
            # "StiffnessModifierMass": "stiffness_modifier_moment_mass",
            # "StiffnessModifierWeight": "stiffness_modifier_moment_weight",
            # "EndFixityAxialStart": "end_fixity_axial_start",
            # "EndFixityShearMajorStart": "end_fixity_shear_major_start",
            # "EndFixityShearMinorStart": "end_fixity_shear_minor_start",
            # "EndFixityTorsionStart": "end_fixity_torsion_start",
            # "EndFixityMomentMajorStart": "end_fixity_moment_major_start",
            # "EndFixityMomentMinorStart": "end_fixity_moment_minor_start",
            # "EndFixityAxialEnd": "end_fixity_axial_end",
            # "EndFixityShearMajorEnd": "end_fixity_shear_major_end",
            # "EndFixityShearMinorEnd": "end_fixity_shear_minor_end",
            # "EndFixityTorsionEnd": "end_fixity_torsion_end/",
            # "EndFixityMomentMajorEnd": "begin_node_y_offset",
            # "EndFixityMomentMinorEnd": "end_node_y_offset",
            # "LateralRestrain": "begin_node",
            # "LateralRestrainLocation": "end_node",
            # "LengthEffectiveMajor": "length",
            # "LengthEffectiveMinor": "local_axis_x",
            # "SwayInMajor": "local_axis_y",
            # "SwayInMinor": "local_axis_z",
            # "BracedAbtMajor": "begin_node_y_offset",
            # "BracedAbtMinor": "end_node_y_offset",
        }

        instance: XmiStructuralCurveMember | None = None
        exceptions: list[Exception] = []
        processed_data: dict = {KEY_MAPPING.get(
            key, key): value for key, value in xmi_dict_obj.items()}

        if cross_section is not None:
            processed_data['cross_section'] = cross_section

        if nodes is not None:
            processed_data['nodes'] = nodes

        if segments is not None:
            processed_data['segments'] = segments

        # if segment_types is not None:
        #     processed_data['segment_types'] = segment_types

        instance, exceptions_found = cls.from_dict(
            processed_data)

        exceptions.extend(exceptions_found)

        return instance, exceptions
