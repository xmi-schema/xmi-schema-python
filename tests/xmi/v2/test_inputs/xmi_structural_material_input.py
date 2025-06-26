valid_material_input = {
    "ID": "7cadcb92-45b2-4ae1-a774-56857a75d7d2",
    "Name": "Concrete - Cast-in-Place Concrete",
    "IFCGUID": "ec1f9186-55b1-40c8-b048-4949f7f76058-0005176d",
    "NativeId": "333677",
    "Description": "",
    "EntityType": "XmiStructuralMaterial",
    "MaterialType": "Concrete",
    "Grade": 35.0,
    "UnitWeight": 2406.534222293481,
    "EModulus": "(9116568000, 9116568000, 9116568000)",
    "GModulus": "(3798722400, 3798722400, 3798722400)",
    "PoissonRatio": "(0.2, 0.2, 0.2)",
    "ThermalCoefficient": 9.9E-06
}

missing_material_type_input = {
    "Grade": 35.0,
    "UnitWeight": 24.0,
    "EModulus": 30000.0
}

invalid_material_type_input = {
    "MaterialType": 123,
    "Grade": "high",
}