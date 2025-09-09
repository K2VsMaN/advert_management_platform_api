from fastapi import FastAPI, HTTPException, status
from bson.objectid import ObjectId
from db import adverts_collection
from utils import replace_advert_id

app = FastAPI()


@app.get(
    "/adverts/{advert_id}",
    tags=["Adverts"],
    summary="Get an advert detail by ID"
)
def get_advert_by_id(advert_id):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    advert = adverts_collection.find_one({"_id": ObjectId(advert_id)})
    return {"data": replace_advert_id(advert)}
