from typing import List, Dict, Any, Optional, Type
from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.schemas.statistics import Statistic, Correlation
from app.utils import parse_list

AVAILABLE_STATISTICS: List[Statistic] = [
    { "name": "basic", "info": "" },
    { "name": "correlation", "info": "" },
]

AVAILABLE_CORRELATIONS: List[Correlation] = [
    { "name": "pearson", "info": "", "reference": "" },
    { "name": "other", "info": "", "reference": "" },
]

def get_router(settings: Settings) -> APIRouter:
    router = APIRouter(
        prefix="/statistics",
        tags=["statistics"],
        responses={404: {"description": "Not found"}},
    )

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
    async def describe(inputs: List[str] = Depends(parse_list(class_type=str, default=None))) -> Dict[str, Any]:
        # do stuff
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

    return router