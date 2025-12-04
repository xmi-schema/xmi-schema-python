from pydantic import Field, model_validator
from typing import Optional
from ..bases.xmi_base_structural_analytical_entity import XmiBaseStructuralAnalyticalEntity

class XmiStorey(XmiBaseStructuralAnalyticalEntity):
    storey_elevation: float = Field(..., alias="StoreyElevation")
    storey_mass: float = Field(..., alias="StoreyMass")
    storey_horizontal_reaction_x: Optional[str] = Field(default=None, alias="StoreyHorizontalReactionX")
    storey_horizontal_reaction_y: Optional[str] = Field(default=None, alias="StoreyHorizontalReactionY")
    storey_vertical_reaction: Optional[str] = Field(default=None, alias="StoreyVerticalReaction")

    @model_validator(mode="before")
    @classmethod
    def inject_entity_type(cls, values):
        values.setdefault("entity_type", "XmiStorey")
        return values

    def __eq__(self, other):
        if not isinstance(other, XmiStorey):
            return NotImplemented
        return self.native_id.lower() == other.native_id.lower()

    def __hash__(self):
        return hash(self.native_id.lower()) if self.native_id else 0
