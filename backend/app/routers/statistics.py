from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel
from fastapi import APIRouter, Depends


#from ..dependencies import get_token_header

def remove_space(s: str):
    """ """
    shorter_string = s
    for space in " \n\t\r":
        shorter_string = shorter_string.replace(space, "")
    return shorter_string

def parse_list(class_type: Type, default: List[Any] = [], separator: str = ","):
    def parser(inputs: str = None) -> Optional[List[class_type]]:
        if inputs is None:
            return default
        # Split the string
        elements = inputs.split(separator)
        # Remove space
        elements = [ remove_space(e) for e in elements if not e.isspace() ]
        # Check the typing
        errors = {}
        results = []
        for idx, el in enumerate(elements):
            try:
                results.append(class_type(el))
            except ValueError as e:
                errors[idx] = repr(e)
        if errors:
            raise Exception(f"Could not parse elements: {errors}")
        else:
            return results
    return parser

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

# --- faire des base models 
class Statistic(BaseModel):
    name: str
    info: str

class Correlation(Statistic):
    reference: str

# --- fin
AVAILABLE_STATISTICS: List[Statistic] = [
    { "name": "basic", "info": "" },
    { "name": "correlation", "info": "" },
]

AVAILABLE_CORRELATIONS: List[Correlation] = [
    { "name": "pearson", "info": "", "reference": "" },
    { "name": "other", "info": "", "reference": "" },
]

fake_datasets_db = [ {'id': f"{i}", 'name': f"dataset {i}", 'path': f'dataset_{i}.csv'} for i in range(20) ]

@router.get("/")
async def root() -> Dict[str, Any]:
    return { "message": "Section for EDA" }

@router.get("/available_statistics")
async def get_available_statistics() -> List[Statistic]:
    return AVAILABLE_STATISTICS

@router.get("/available_correlations")
async def get_available_correlations() -> List[Correlation]:
    return AVAILABLE_CORRELATIONS

@router.get("/type/")
async def get_type(inputs: List[str] = Depends(parse_list(class_type=str)) ) -> Dict[str, Any]:
    # do stuff
    if inputs:
        return {"message": f"Type for some inputs: {inputs}"}
    else:
        return {"message": "Type for all inputs"}

@router.get("/describe/")
async def describe(inputs: str = None) -> Dict[str, Any]:
    # do stuff inputs should be List[str]
    if inputs is None:
        return {"message": "Describe all the data"}
    else:
        return {"message": "Describe some inputs: {inputs}"}

@router.get("/correlation/")
async def get_correlation(input1: str = None, input2: str = None)-> Dict[str, Any]:
    # do stuff -- add type of correlation
    if input1 and input2:
        return {"message": f"Correlation between {input1} and {input2}"}
    else:
        return {"message": "Correlation between all inputs"}
