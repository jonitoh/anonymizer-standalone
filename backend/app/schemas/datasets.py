from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
 
class Dataset(BaseModel):
    id: str
    name: str
    path: Path

class DatasetName(BaseModel):
    id: str
    name: str

class MetadataField(BaseModel):
    input: str = None
    type: str = None
    info: str = Field(None, description="free text")

class Metadata(BaseModel):
    id: str
    dataset_id: str
    inputs: List[MetadataField]