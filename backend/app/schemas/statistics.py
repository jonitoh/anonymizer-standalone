from pydantic import BaseModel, Field

class Statistic(BaseModel):
    name: str
    info: str

class Correlation(Statistic):
    reference: str = Field(..., title="reference to lookup in case of ambiguity")
