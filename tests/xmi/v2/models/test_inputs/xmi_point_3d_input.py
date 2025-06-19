import uuid

valid_point_input = {
    "ID": str(uuid.uuid4()),
    "Name": "Test Point",
    "X": 1.23,
    "Y": 4.56,
    "Z": 7.89,
    "Description": "A valid 3D point",
    "IFCGUID": "abc-123-def"
}

missing_z_input = {
    "ID": str(uuid.uuid4()),
    "Name": "Incomplete Point",
    "X": 1.23,
    "Y": 4.56,
    "Description": "Missing Z coordinate",
    "IFCGUID": "xyz-789"
}

invalid_x_input = {
    "ID": str(uuid.uuid4()),
    "Name": "Invalid Point",
    "X": "not a number",
    "Y": 4.56,
    "Z": 7.89,
    "Description": "X is invalid",
    "IFCGUID": "invalid-001"
}