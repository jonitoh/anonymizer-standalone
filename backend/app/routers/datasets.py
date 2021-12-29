from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from ..dependencies import get_token_header


router = APIRouter(

    prefix="/datasets",

    tags=["datasets"],

    dependencies=[],#Depends(get_token_header)],

    responses={404: {"description": "Not found"}},

)



fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}



@router.get("/")

async def read_items():
    return fake_items_db



@router.get("/{item_id}")

async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

@router.post("/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# @router.post("/")
# async def receive_file(file: UploadFile = File(...)):
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     filename = f'{dir_path}/uploads/{time.time()}-{file.filename}'
#     f = open(f'{filename}', 'wb')
#     content = await file.read()
#     f.write(content)



@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
