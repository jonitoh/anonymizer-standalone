from typing import List, Dict, Any
import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter


#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

# --- faire des base models 
class Statistic(BaseModel):
    name: str
    info: str

# --- fin
AVAILABLE_STATISTICS: List[Statistic] = [
    { "name": "basic", "info": "" },
    { "name": "correlation", "info": "" },
]
fake_datasets_db = [ {'id': f"{i}", 'name': f"dataset {i}", 'path': f'dataset_{i}.csv'} for i in range(20) ]

def retrieve_dataset(dataset_id: str):
    if dataset_id not in set([ k['id'] for k in fake_datasets_db]):
        return None #raise Error("Dataset not found")
    document = [ k for k in fake_datasets_db if k['id'] == dataset_id ][0]
    return pd.read_csv(document['path'])

@router.get("/type/")
async def get_type(input: str = None)-> Dict[str, Any]:
    # do stuff
    if input:
        return {"message": f"Type for the specific input {input}"}
    else:
        return {"message": "Type for all inputs"}

@router.get("/describe/")
async def describe(inputs: str = None) -> Dict[str, Any]:
    # do stuff inputs should be List[str]
    if inputs is None:
        return {"message": "Describe all the data"}
    else:
        return {"message": "Describe some inputs"}

@router.get("/correlation/")
async def get_correlation(input1: str = None, input2: str = None)-> Dict[str, Any]:
    # do stuff -- add type of correlation
    if input1 and input2:
        return {"message": f"Correlation between {input1} and {input2}"}
    else:
        return {"message": "Correlation between all inputs"}

@router.get("/available_statistics")
async def get_available_statistics() -> List[Statistic]:
    return AVAILABLE_STATISTICS
