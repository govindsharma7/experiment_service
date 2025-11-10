from pydantic import BaseModel, Field

class ExperimentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the experiment")