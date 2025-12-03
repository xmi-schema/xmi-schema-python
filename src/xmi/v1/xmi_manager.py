# Optional, for forward declarations in Python 3.7+
from __future__ import annotations


from .entities.xmi_segment import XmiSegment

from .entities.xmi_structural_cross_section import XmiCrossSection
from .entities.xmi_structural_point_connection import XmiStructuralPointConnection
from .entities.xmi_structural_material import XmiStructuralMaterial
from .entities.xmi_structural_curve_member import XmiStructuralCurveMember
from .entities.xmi_structural_surface_member import XmiStructuralSurfaceMember

from .xmi_model import XmiModel, ErrorLog
from .geometries.xmi_point_3d import XmiPoint3D
from .geometries.xmi_line_3d import XmiLine3D
from .geometries.xmi_arc_3d import XmiArc3D
from .geometries.xmi_base_geometry import XmiBaseGeometry

from .relationships.xmi_has_structural_material import XmiHasStructuralMaterial
from .relationships.xmi_has_structural_node import XmiHasStructuralNode
from .relationships.xmi_has_structural_cross_section import XmiHasCrossSection
from .relationships.xmi_has_segment import XmiHasSegment
from .relationships.xmi_has_geometry import XmiHasGeometry

from .xmi_errors import *
from .xmi_base import XmiBaseEntity
from .enums.xmi_enums import XmiSegmentTypeEnum

SEGMENT_TYPE_MAPPING = {
    XmiSegmentTypeEnum.LINE: XmiLine3D,
    XmiSegmentTypeEnum.CIRCULAR_ARC: XmiArc3D
}


class XmiManager():

    def __init__(self):
        self.models = []

    def _rearrange_xmi_dict(self, xmi_dict: dict) -> dict:
        # Define the desired key order
        desired_order = ['StructuralMaterial',
                         'StructuralPointConnection',
                         'StructuralCrossSection',
                         'StructuralCurveMember',
                         'StructuralSurfaceMember'
                         ]
        # Create a new dictionary with rearranged keys
        rearranged_xmi_dict = {key: xmi_dict[key]
                               for key in desired_order if key in xmi_dict.keys()}

        # Add keys not in the desired order
        rearranged_xmi_dict.update(
            {key: value for key, value in xmi_dict.items() if key not in desired_order})

        return rearranged_xmi_dict

    def read_xmi_dict(self, xmi_dict: dict) -> XmiModel:
        xmi_model = XmiModel()

        # 1. rearrange the dictionary first
        rearranged_xmi_dict = self._rearrange_xmi_dict(xmi_dict)

        # 2. iterate through all the keys to generate entities
        for xmi_dict_key, xmi_dict_value in rearranged_xmi_dict.items():
            if xmi_dict_key == "StructuralMaterial":
                for index, xmi_structural_material_obj in enumerate(xmi_dict_value):
                    try:
                        xmi_structural_material, error_logs = XmiStructuralMaterial.from_xmi_dict_obj(
                            xmi_structural_material_obj)
                        if xmi_structural_material:
                            xmi_model.entities.append(xmi_structural_material)
                        xmi_model.errors.extend(error_logs)
                    except Exception as e:
                        xmi_model.errors.append(
                            ErrorLog(xmi_dict_key, index, str(e)))
                # check for duplicates after all xmi_structural_material_objs have been instantiated

            if xmi_dict_key == "StructuralPointConnection":
                for index, xmi_structural_point_connection_obj in enumerate(xmi_dict_value):
                    try:
                        xmi_point_3d, error_logs = XmiPoint3D.from_xmi_dict_obj(
                            xmi_structural_point_connection_obj)
                        xmi_structural_point_connection_obj['point'] = xmi_point_3d
                        xmi_structural_point_connection, error_logs = XmiStructuralPointConnection.from_xmi_dict_obj(
                            xmi_structural_point_connection_obj)

                        if xmi_structural_point_connection:
                            xmi_model.entities.append(
                                xmi_structural_point_connection)
                            xmi_model.entities.append(xmi_point_3d)
                            xmi_model.create_relationship(
                                XmiHasGeometry, xmi_structural_point_connection, xmi_point_3d)

                        xmi_model.errors.extend(error_logs)
                    except Exception as e:
                        xmi_model.errors.append(
                            ErrorLog(xmi_dict_key, index, str(e)))
                # check for duplicate names and id after all xmi_structural_point_connection_objs have been instantiated

            if xmi_dict_key == "StructuralCrossSection":
                for index, xmi_structural_cross_section_obj in enumerate(xmi_dict_value):
                    try:
                        xmi_structural_material_found_in_xmi_manager = None

                        if 'Material' not in xmi_structural_cross_section_obj:
                            raise XmiMissingReferenceInstanceError(
                                "Material Attribute in xmi_dict is missing")

                        xmi_structural_material_name_to_find: str = xmi_structural_cross_section_obj[
                            'Material']
                        xmi_structural_material_found_in_xmi_manager = next(
                            (inst for inst in xmi_model.entities
                                if inst.name == xmi_structural_material_name_to_find
                                and isinstance(inst, XmiStructuralMaterial)),
                            None
                        )

                        xmi_structural_cross_section, error_logs = XmiCrossSection.from_xmi_dict_obj(
                            xmi_structural_cross_section_obj,
                            material=xmi_structural_material_found_in_xmi_manager
                        )
                        xmi_model.errors.extend(error_logs)
                        if xmi_structural_cross_section and isinstance(xmi_structural_cross_section, XmiCrossSection):
                            xmi_model.entities.append(
                                xmi_structural_cross_section)
                            xmi_model.create_relationship(
                                XmiHasStructuralMaterial, xmi_structural_cross_section, xmi_structural_cross_section.material)

                    except Exception as e:
                        xmi_model.errors.append(
                            ErrorLog(xmi_dict_key, index, str(e)))

            if xmi_dict_key == "StructuralCurveMember":
                for index, xmi_structural_curve_member_obj in enumerate(xmi_dict_value):
                    try:
                        xmi_structural_cross_section_found_in_xmi_manager = None

                        # find referenced cross section
                        if 'CrossSection' not in xmi_structural_curve_member_obj:
                            raise XmiMissingReferenceInstanceError(
                                "CrossSection Attribute in xmi_dict is missing")

                        xmi_structural_cross_section_name_to_find: str = xmi_structural_curve_member_obj[
                            'CrossSection']

                        xmi_structural_cross_section_found_in_xmi_manager = next(
                            (inst for inst in xmi_model.entities
                                if inst.name == xmi_structural_cross_section_name_to_find
                                and isinstance(inst, XmiCrossSection)), None)

                        # find referenced structural_point_connections
                        xmi_structural_point_connections_name_str_to_find: str = xmi_structural_curve_member_obj[
                            'Nodes']

                        xmi_structural_point_connections_found_in_xmi_manager = []

                        xmi_structural_point_connections_name_list_to_find: list[str] = xmi_structural_point_connections_name_str_to_find.split(
                            ";")

                        for xmi_structural_point_connection_name in xmi_structural_point_connections_name_list_to_find:
                            xmi_structural_point_connection_found_in_xmi_manager = None
                            xmi_structural_point_connection_found_in_xmi_manager = next(
                                (inst for inst in xmi_model.entities
                                    if inst.name == xmi_structural_point_connection_name
                                    and isinstance(inst, XmiStructuralPointConnection)), None)
                            xmi_structural_point_connections_found_in_xmi_manager.append(
                                xmi_structural_point_connection_found_in_xmi_manager)

                        # find segments within structural_curve_member
                        xmi_segments_str_to_find: str = xmi_structural_curve_member_obj['Segments']
                        xmi_segments_list_to_find: list[str] = xmi_segments_str_to_find.split(
                            ";")
                        # check segments validity, need to rectify. can accept multiple segments
                        if len(xmi_segments_list_to_find) > 1:
                            exception_found = ValueError(
                                "Segments Key should only have 1 segment for {xmi_structural_curve_member_obj}".format(xmi_structural_curve_member_obj=str(xmi_structural_curve_member_obj)))
                            xmi_model.errors.append(
                                ErrorLog(xmi_dict_key, index, str(exception_found)))
                            pass

                        xmi_segments_found_in_xmi_manager: list[XmiSegment] = [
                        ]
                        for index, xmi_segment_name_to_find in enumerate(xmi_segments_list_to_find):

                            xmi_geometry_class_found: XmiBaseEntity | None = None

                            # find segment_type
                            xmi_segment_type_found: XmiSegmentTypeEnum = XmiSegmentTypeEnum.from_attribute_get_enum(
                                xmi_segment_name_to_find)
                            # if segment type exist. find and create geometry_element
                            xmi_geometry_class_found = SEGMENT_TYPE_MAPPING[xmi_segment_type_found] if xmi_segment_type_found in SEGMENT_TYPE_MAPPING.keys(
                            ) else None

                            begin_node_found: XmiStructuralPointConnection = xmi_structural_point_connections_found_in_xmi_manager[
                                index]
                            end_node_found: XmiStructuralPointConnection = xmi_structural_point_connections_found_in_xmi_manager[
                                index + 1]

                            try:

                                geometry_found: XmiBaseGeometry = xmi_geometry_class_found(start_point=begin_node_found.point,
                                                                                           end_point=end_node_found.point)

                                xmi_segment_found = XmiSegment(geometry=geometry_found,
                                                               position=index + 1,
                                                               begin_node=begin_node_found,
                                                               end_node=end_node_found,
                                                               segment_type=xmi_segment_type_found,
                                                               )
                                if xmi_segment_found is not None:
                                    xmi_segments_found_in_xmi_manager.append(
                                        xmi_segment_found)
                                    xmi_model.entities.append(
                                        xmi_segment_found.geometry)
                                    xmi_model.entities.append(
                                        xmi_segment_found)
                                    xmi_model.create_relationship(
                                        XmiHasGeometry, geometry_found, geometry_found.start_point, is_begin=True)
                                    xmi_model.create_relationship(
                                        XmiHasGeometry, geometry_found, geometry_found.end_point, is_end=True)

                            except Exception as e:
                                xmi_model.errors.append(
                                    ErrorLog(xmi_dict_key, index, str(e)))
                                pass

                        # create_segment

                        xmi_structural_curve_member, error_logs = XmiStructuralCurveMember.from_xmi_dict_obj(
                            xmi_structural_curve_member_obj,
                            cross_section=xmi_structural_cross_section_found_in_xmi_manager,
                            nodes=xmi_structural_point_connections_found_in_xmi_manager,
                            segments=xmi_segments_found_in_xmi_manager,
                        )

                        xmi_model.errors.extend(error_logs)
                        if xmi_structural_curve_member:
                            xmi_model.entities.append(
                                xmi_structural_curve_member)
                            xmi_model.create_relationship(
                                XmiHasCrossSection, xmi_structural_curve_member, xmi_structural_curve_member.cross_section)
                            for segment in xmi_structural_curve_member.segments:
                                xmi_model.create_relationship(
                                    XmiHasSegment, xmi_structural_curve_member, segment)
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, segment, segment.begin_node, is_begin=True)
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, segment, segment.end_node, is_end=True)
                                xmi_model.create_relationship(
                                    XmiHasGeometry, segment, segment.geometry)

                            for spc in xmi_structural_curve_member.nodes:
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, xmi_structural_curve_member, spc)

                    except Exception as e:
                        xmi_model.errors.append(
                            ErrorLog(xmi_dict_key, index, str(e), obj=xmi_structural_curve_member_obj))

            if xmi_dict_key == "StructuralSurfaceMember":
                for index, xmi_structural_surface_member_obj in enumerate(xmi_dict_value):
                    try:
                        # find referenced structural_material
                        xmi_structural_material_found_in_xmi_manager = None

                        # find referenced cross section
                        if 'Material' not in xmi_structural_surface_member_obj:
                            raise XmiMissingReferenceInstanceError(
                                "Material Attribute in xmi_dict is missing")

                        xmi_structural_material_name_to_find: str = xmi_structural_surface_member_obj[
                            'Material']

                        xmi_structural_material_found_in_xmi_manager = next(
                            (inst for inst in xmi_model.entities
                                if inst.name == xmi_structural_material_name_to_find
                                and isinstance(inst, XmiStructuralMaterial)), None)

                        # find referenced structural_point_connections
                        xmi_structural_point_connections_name_str_to_find: str = xmi_structural_surface_member_obj[
                            'Nodes']

                        xmi_structural_point_connections_found_in_xmi_manager = []

                        xmi_structural_point_connections_name_list_to_find: list[str] = xmi_structural_point_connections_name_str_to_find.split(
                            ";")

                        for xmi_structural_point_connection_name in xmi_structural_point_connections_name_list_to_find:
                            xmi_structural_point_connection_found_in_xmi_manager = None
                            xmi_structural_point_connection_found_in_xmi_manager = next(
                                (inst for inst in xmi_model.entities
                                    if inst.name == xmi_structural_point_connection_name
                                    and isinstance(inst, XmiStructuralPointConnection)), None)
                            xmi_structural_point_connections_found_in_xmi_manager.append(
                                xmi_structural_point_connection_found_in_xmi_manager)

                        # find segments within structural_curve_member
                        xmi_segments_str_to_find: str = xmi_structural_surface_member_obj[
                            'Edges']
                        xmi_segments_list_to_find: list[str] = xmi_segments_str_to_find.split(
                            ";")
                        # check segments validity
                        if len(xmi_segments_list_to_find) < 3:
                            exception_found = ValueError(
                                "Segments Key should at least have 3 segment for {xmi_structural_surface_member_obj}".format(xmi_structural_surface_member_obj=str(xmi_structural_surface_member_obj)))
                            xmi_model.errors.append(
                                ErrorLog(xmi_dict_key, index, str(exception_found)))
                            pass

                        xmi_segments_found_in_xmi_manager: list[XmiSegment] = [
                        ]
                        for index, xmi_segment_name_to_find in enumerate(xmi_segments_list_to_find):
                            # find segment_type
                            xmi_segment_type_found: XmiSegmentTypeEnum = XmiSegmentTypeEnum.from_attribute_get_enum(
                                xmi_segment_name_to_find)
                            # if segment type exist. find and create geometry_element
                            xmi_geometry_class_found = SEGMENT_TYPE_MAPPING[xmi_segment_type_found] if xmi_segment_type_found in SEGMENT_TYPE_MAPPING.keys(
                            ) else None

                            # if segment type exist. find and create geometry_element
                            begin_node_found = xmi_structural_point_connections_found_in_xmi_manager[
                                index]
                            end_node_found = None

                            # current implementation assumes the last node found is also the first node to create a closed surface.
                            if index < (len(xmi_segments_list_to_find) - 1):
                                end_node_found = xmi_structural_point_connections_found_in_xmi_manager[
                                    index + 1]
                            else:
                                end_node_found = xmi_structural_point_connections_found_in_xmi_manager[
                                    0]

                            try:
                                geometry_found = xmi_geometry_class_found(start_point=begin_node_found.point,
                                                                          end_point=end_node_found.point)
                                xmi_segment_found = XmiSegment(geometry=geometry_found,
                                                               position=index + 1,
                                                               begin_node=begin_node_found,
                                                               end_node=end_node_found,
                                                               segment_type=xmi_segment_type_found,
                                                               )
                                if xmi_segment_found is not None:
                                    xmi_segments_found_in_xmi_manager.append(
                                        xmi_segment_found)
                                    xmi_model.entities.append(
                                        xmi_segment_found)
                                    xmi_model.entities.append(
                                        xmi_segment_found.geometry)
                                    xmi_model.create_relationship(
                                        XmiHasGeometry, geometry_found, geometry_found.start_point, is_begin=True)
                                    xmi_model.create_relationship(
                                        XmiHasGeometry, geometry_found, geometry_found.end_point, is_end=True)
                                    xmi_model.create_relationship(
                                        XmiHasGeometry, segment, segment.geometry)

                            except Exception as e:
                                xmi_model.errors.append(
                                    ErrorLog(xmi_dict_key, index, str(e)))
                                pass

                        xmi_structural_surface_member, error_logs = XmiStructuralSurfaceMember.from_xmi_dict_obj(
                            xmi_dict_obj=xmi_structural_surface_member_obj,
                            material=xmi_structural_material_found_in_xmi_manager,
                            nodes=xmi_structural_point_connections_found_in_xmi_manager,
                            segments=xmi_segments_found_in_xmi_manager
                        )

                        xmi_model.errors.extend(error_logs)
                        if xmi_structural_surface_member:
                            xmi_model.entities.append(
                                xmi_structural_surface_member)
                            xmi_model.create_relationship(
                                XmiHasStructuralMaterial, xmi_structural_surface_member, xmi_structural_surface_member.material)
                            for segment in xmi_structural_surface_member.segments:
                                xmi_model.create_relationship(
                                    XmiHasSegment, xmi_structural_surface_member, segment)
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, segment, segment.begin_node, is_begin=True)
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, segment, segment.end_node, is_end=True)

                            for spc in xmi_structural_surface_member.nodes:
                                xmi_model.create_relationship(
                                    XmiHasStructuralNode, xmi_structural_surface_member, spc)

                    except Exception as e:
                        xmi_model.errors.append(
                            ErrorLog(xmi_dict_key, index, str(e), obj=xmi_structural_surface_member_obj))

        self.models.append(xmi_model)

        return xmi_model
