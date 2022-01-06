import os
from pathlib import Path
import mimetypes
from datetime import datetime
import random
from typing import List, Dict, Union
import pandas as pd
from pydantic import BaseModel, Json, Field
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse


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
# --- fin

fake_datasets_db: List[Dataset] = [ {'id': f"{i}", 'name': f"dataset {i}", 'path': Path(f'dataset_{i}.csv')} for i in range(20) ]

def retrieve_dataset(dataset_id: str):
    # TODO: to remove
    if dataset_id not in set([ k['id'] for k in fake_datasets_db]):
        return None #raise Error("Dataset not found")
    document = [ k for k in fake_datasets_db if k['id'] == dataset_id ][0]
    return pd.read_csv(document['path'])

DEFAULT_MEDIA_TYPE: str = 'application/octet-stream'

def retrieve_file(path: Path, media_type: str = None, infer_media_type: bool = False):
    """cf. https://fastapi.tiangolo.com/advanced/custom-response/
    cf. https://cloudbytes.dev/snippets/received-return-a-file-from-in-memory-buffer-using-fastapi
    cf. https://stackoverflow.com/questions/61140398/fastapi-return-a-file-response-with-the-output-of-a-sql-query
    """
    # check path is ok
    if path is None:
        return "no"
    # check media_type
    if media_type is None or infer_media_type:
        media_type, _ = mimetypes.guess_type(path)
        if media_type is None:
            media_type = DEFAULT_MEDIA_TYPE
    # generate filename
    filename = 'test_' + path.name
    # generator based on our file
    def iterfile(): 
        with open(path, mode="rb") as file_like: 
            yield from file_like

    response = StreamingResponse(
        content=iterfile(),
        media_type=media_type,
    )

    response.headers["Content-Disposition"] = f"attachment;filename={filename}"
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    return response
 
@router.get("/", summary="summary", response_description="the wanted dataset")
async def get_datasets(limit: int = 3) -> List[Dataset]:
    """
    RETRIEVE DATASET
    """
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
async def get_dataset(dataset_id: str, only_file: bool = False) -> Union[Dataset, str]:
    if dataset_id not in set([ k['id'] for k in fake_datasets_db]):
        raise HTTPException(status_code=404, detail="Dataset not found")
    document = [ k for k in fake_datasets_db if k['id'] == dataset_id ][0]
    if only_file:
        return retrieve_file(document["path"])
    else:
        return document
 

@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: str) -> Dict[str, str]:
    global fake_datasets_db
    print("dataset_id?", dataset_id)
    if dataset_id not in set([ k['id'] for k in fake_datasets_db ]):
        raise HTTPException(status_code=404, detail="Dataset not found")
    my_dataset = [ k for k in fake_datasets_db if k['id'] == dataset_id ][0]
    fake_datasets_db = [ k for k in fake_datasets_db if k['id'] != dataset_id ]
    # remove the file
    if Path(my_dataset['path']).exists():
        Path(my_dataset['path']).unlink()
    else:
        print("strange! the path does not exist")
    return {'message': 'ok'}

# No update allowed
# @router.put("/")

@router.post("/")
async def create_dataset(
    dataset: UploadFile = File(...),
    metadata: Json[Dict[str, MetadataField]] = None,# workaround so that the metadatafield form field pass through. cf.https://github.com/tiangolo/fastapi/issues/2387 
    name: str = None) -> Dict[str, str]:
    global fake_datasets_db
    print("metadata??", metadata)
    # -- dataset
    dataset_message = ""
    filename = Path(dataset.filename)
    # verify if the size is ok
    # size = ????
    # print("size", size)
    # if size > TOO_LARGE_FILE_SIZE:
    #     raise HTTPException(status_code=404, detail="Dataset file too heavy")
    # check for a valid Name
    if name is None:
        name = filename.name
    # create a document
    # find an id
    available_ids = [ k['id'] for k in fake_datasets_db]
    chosen_id = str(random.choice([e for e in range(10000) if e not in available_ids ]))
    # save dataset in local storage
    path = Path(
        Path.cwd(),
        UPLOAD_FOLDER,
        f'{datetime.now().strftime(DATETIME_FORMAT_FOR_UPLOAD)}___{filename}'
    )
    #print("######", path)
    document_dataset = {'id': chosen_id, 'name': name, 'path': Path(path)}
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
    inputs = []
    if metadata is None: # second option: None equivalent inferred by FASTAPI
        inputs = [{'input': f'Field {i}', 'type': random.choice(['numerical', 'binary', 'categorical']), 'info': 'nope'} for i in range(random.randint(1, 4))]
    else:
        inputs = metadata
    # find an id
    metadata_id = str(random.randint(0, 10000))
    document_metadata = {'id': metadata_id, 'dataset_id': chosen_id, 'inputs': inputs }
    print("doc metadata", document_metadata)
    metadata_message = "ok"
    # document metadata in mongo
    fake_datasets_db.append(document_dataset)

    return {"id": chosen_id, "dataset_message": dataset_message, "metadata_message": metadata_message}
