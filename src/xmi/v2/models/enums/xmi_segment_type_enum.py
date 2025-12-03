from enum import unique
from ..bases.xmi_base_enum import XmiBaseEnum

@unique
class XmiSegmentTypeEnum(XmiBaseEnum):
    """
    Enumeration of geometric segment types used in structural members.

    This enum defines the types of geometric segments that represent the path
    between nodes in structural members (beams, columns, etc.). The segment type
    determines how the geometry is represented mathematically and which geometry
    class is used to store the segment data.

    Attributes:
        LINE: Straight line segment (most common)
        CIRCULAR_ARC: Circular arc segment for curved members
        PARABOLIC_ARC: Parabolic arc segment (not yet implemented)
        BEZIER: Bezier curve segment (not yet implemented)
        SPLINE: Spline curve segment (not yet implemented)
        OTHERS: Other custom segment types (not yet implemented)

    Examples:
        >>> from xmi.v2.models.enums.xmi_segment_type_enum import XmiSegmentTypeEnum
        >>> # Direct access
        >>> seg_type = XmiSegmentTypeEnum.LINE
        >>> print(seg_type.value)  # "Line"
        >>>
        >>> # Case-insensitive lookup
        >>> seg_type = XmiSegmentTypeEnum("circular arc")  # Returns CIRCULAR_ARC
        >>>
        >>> # Get geometry class for segment type
        >>> geom_class = XmiSegmentTypeEnum.LINE.get_geometry_class()
        >>> print(geom_class)  # <class 'XmiLine3D'>

    Note:
        Only LINE and CIRCULAR_ARC have implemented geometry classes.
        Other segment types will return None from get_geometry_class().
    """
    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    PARABOLIC_ARC = "Parabolic Arc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
    OTHERS = "Others"

    def get_geometry_class(self):
        """
        Get the geometry class associated with this segment type.

        This method maps segment types to their corresponding geometry classes
        used to represent the segment's geometric data.

        Returns:
            type or None: The geometry class (XmiLine3D, XmiArc3D) if implemented,
                         None if not yet implemented for this segment type.

        Examples:
            >>> seg_type = XmiSegmentTypeEnum.LINE
            >>> geom_class = seg_type.get_geometry_class()
            >>> print(geom_class)  # <class 'XmiLine3D'>
            >>>
            >>> seg_type = XmiSegmentTypeEnum.CIRCULAR_ARC
            >>> geom_class = seg_type.get_geometry_class()
            >>> print(geom_class)  # <class 'XmiArc3D'>
            >>>
            >>> seg_type = XmiSegmentTypeEnum.BEZIER
            >>> geom_class = seg_type.get_geometry_class()
            >>> print(geom_class)  # None (not implemented)
        """
        from ..geometries.xmi_line_3d import XmiLine3D
        from ..geometries.xmi_arc_3d import XmiArc3D

        mapping = {
            XmiSegmentTypeEnum.LINE: XmiLine3D,
            XmiSegmentTypeEnum.CIRCULAR_ARC: XmiArc3D,
        }
        return mapping.get(self)
    