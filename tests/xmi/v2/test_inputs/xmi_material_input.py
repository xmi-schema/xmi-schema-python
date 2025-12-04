valid_material_input = {
    "ID": "mat-001",
    "Name": "C35 Concrete",
    "MaterialType": "Concrete",
    "Grade": 35.0,
    "UnitWeight": 24.5,
    "EModulus": "(30000, 30000, 30000)",
    "GModulus": "(12300, 12300, 12300)",
    "PoissonRatio": "(0.2, 0.2, 0.2)",
    "ThermalCoefficient": 1.2e-5,
}

missing_material_type_input = {
    "ID": "mat-002",
    "Name": "Unknown Material",
    "Grade": 20.0,
}

invalid_material_type_input = {
    "ID": "mat-003",
    "Name": "Plastic",
    "MaterialType": "Plastic",
}
