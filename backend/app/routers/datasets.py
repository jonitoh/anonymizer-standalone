import os
from datetime import datetime
import random
from typing import List, Dict
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, UploadFile, File


#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)
TOO_LARGE_FILE_SIZE = 10000000
UPLOAD_FOLDER = 'uploads'
DATETIME_FORMAT_FOR_UPLOAD = "%Y-%m-%d-%H-%M"

# --- faire des base models 
class Dataset(BaseModel):
    id: str
    name: str
    path: str

class DatasetName(BaseModel):
    id: str
    name: str

class MetadataField(BaseModel):
    field: str
    type: str
    info: str

class Metadata(BaseModel):
    id: str
    dataset_id: str
    fields: List[MetadataField]
# --- fin

fake_datasets_db = [ {'id': f"{i}", 'name': f"dataset {i}", 'path': f'dataset_{i}.csv'} for i in range(20) ]


@router.get("/")
async def get_datasets(limit: int = 3) -> List[Dataset]:
    if limit == -1:
        return fake_datasets_db
    else:
        return fake_datasets_db[:limit]

@router.get("/names")
async def get_dataset_names()-> List[DatasetName]:
    return [ {'id': k['id'], 'name': k["name"]} for k in fake_datasets_db ]

@router.get("/size")
async def get_size() -> Dict[str, int]:
    return { 'size': len(fake_datasets_db) }

@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str) -> Dataset:
    if dataset_id not in set([ k['id'] for k in fake_datasets_db]):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return [ k for k in fake_datasets_db if k['id'] == dataset_id ][0]

@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: str) -> Dict[str, str]:
    global fake_datasets_db
    if dataset_id not in set([ k['id'] for k in fake_datasets_db ]):
        raise HTTPException(status_code=404, detail="Dataset not found")
    fake_datasets_db = [ k for k in fake_datasets_db if k['id'] != dataset_id ]
    return {'message': 'ok'}

# No update allowed
# @router.put("/")

@router.post("/")
async def create_dataset(
    dataset: UploadFile = File(...),
    metadata: UploadFile = File(...),# List[MetadataField] = [],
    name: str = None) -> Dict[str, str]:
    # -- dataset
    dataset_message = ""
    # verify if the size is ok
    # size = ????
    # print("size", size)
    # if size > TOO_LARGE_FILE_SIZE:
    #     raise HTTPException(status_code=404, detail="Dataset file too heavy")
    # check for a valid Name
    if name is None:
        name, _ = os.path.splitext(dataset.filename)
        name = os.path.basename(name)
    print("name", name)
    # create a document
    # find an id
    available_ids = [ k['id'] for k in fake_datasets_db]
    chosen_id = str(random.choice([e for e in range(10000) if e not in available_ids ]))
    # save dataset in local storage
    path = os.path.realpath(__file__).split(os.path.sep)[:-3] + [
        UPLOAD_FOLDER,
        f'{datetime.now().strftime(DATETIME_FORMAT_FOR_UPLOAD)}___{dataset.filename}'
    ]
    path = os.path.sep.join(path)

    document_dataset = {'id': chosen_id, 'name': name, 'path': path}
    print("doc dataset", document_dataset)
    dataset_message = "ok"
    # document in mongo -- DONE
    f = open(path, 'wb')
    content = await dataset.read()
    f.write(content)
    # -- metadata
    metadata_message = ""
    # verify if the size is ok
    # size = ????
    # if size > TOO_LARGE_FILE_SIZE:
    #    metadata_message = "Metadata file too heavy"
    # create a document for metadata
    # from csv to metadata or from nada to metadata
    fields = [{'field': f'Field {i}', 'type': random.choice(['numerical', 'binary', 'categorical']), 'info': 'nope'} for i in range(random.randint(1, 4))]
    # find an id
    metadata_id = str(random.randint(0, 10000))
    document_metadata = {'id': metadata_id, 'dataset_id': chosen_id, 'fields': fields }
    print("doc metadata", document_metadata)
    metadata_message = "ok"
    # document metadata in mongo -- DONE

    return {"id": chosen_id, "dataset_message": dataset_message, "metadata_message": metadata_message}
