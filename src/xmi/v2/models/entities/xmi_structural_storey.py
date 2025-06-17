from pydantic import Field
from ..bases.xmi_base_entity import XmiBaseEntity

class XmiStructuralStorey(XmiBaseEntity):
    storey_elevation: float = Field(..., alias="StoreyElevation")

	

# Testing run python -m src.xmi.v2.models.entities.xmi_structural_storey
if __name__ == "__main__":
	def test_xmi_structural_storey():
		storey = XmiStructuralStorey(
            id="storey001",
            name="Ground Floor",
            storey_elevation=0.0
        )
		print("Created XmiStructuralStorey:")
		print(storey.model_dump(by_alias=True))
		
	test_xmi_structural_storey()
