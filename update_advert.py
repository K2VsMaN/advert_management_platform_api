from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from db import adverts_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId
from typing import Annotated
from utils import replace_advert_id

app = FastAPI()

@app.patch("/adverts/{advert_id}")
def update_advert_by_id(
    advert_id: str,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    category: Annotated[str, Form()],
    price: Annotated[float, Form()]):
    try:
        advert_object_id = ObjectId(advert_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_fields = {}
    if title:
        update_fields["title"] = title
    if description:
        update_fields["description"] = description
    if category:
        update_fields["category"] = category
    if price:
        update_fields["price"] = price
    if flyer:
        update_fields["flyer"] = flyer

    updated_advert_result = adverts_collection.update_one(
        {"_id": advert_object_id},
        {"$set": update_fields}
    )

    if updated_advert_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Advert not found")
    
    updated_advert = adverts_collection.find_one({"_id": advert_object_id})

    return {"message": f"Advert {advert_id} updated successfully",
            "advert": replace_advert_id(updated_advert)
            }