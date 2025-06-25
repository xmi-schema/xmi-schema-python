from xmi.v2.models.geometries.xmi_point_3d import XmiPoint3D

valid_line_input = {
    "start_point": {
        "ID": "pt1",
        "Name": "Start Point",
        "X": 1.23,
        "Y": 4.56,
        "Z": 7.89,
        "Description": "Line start",
        "IFCGUID": "guid-start"
    },
    "end_point": {
        "ID": "pt2",
        "Name": "End Point",
        "X": 9.87,
        "Y": 6.54,
        "Z": 3.21,
        "Description": "Line end",
        "IFCGUID": "guid-end"
    }
}

missing_end_input = {
    "start_point": XmiPoint3D(
        ID="pt1",
        Name="Start Point",
        X=1.23,
        Y=4.56,
        Z=7.89,
        Description="Line start",
        IFCGUID="guid-start"
    )
}

invalid_start_point_input = {
    "start_point": {"not": "a point object"},
    "end_point": XmiPoint3D(
        ID="pt2",
        Name="End Point",
        X=9.87,
        Y=6.54,
        Z=3.21,
        Description="Line end",
        IFCGUID="guid-end"
    )
}