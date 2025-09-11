from fastapi import FastAPI, HTTPException, Form, File, UploadFile, status
from db import adverts_collection
from bson.objectid import ObjectId
from typing import Annotated
import cloudinary
import cloudinary.uploader
from datetime import date, time

cloudinary.config(
    cloud_name="dwlcmfaxi",
    api_key="453953172262744",
    api_secret="aQ7PWP7XnvGBlHJ5O0BRL07Xvec"
)

app = FastAPI()

@app.put("/adverts/{advert_id}")
def update_advert_by_id(
    advert_id: str,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    category: Annotated[str, Form()],
    price: Annotated[float, Form()],
    advert_date: Annotated[date, Form(...)],
    start_time: Annotated[time, Form(...)],
    end_time: Annotated[time, Form(...)]):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid ID format")
    
    
    
    upload_result = cloudinary.uploader.upload(flyer.file)
    adverts_collection.replace_one(
        filter={"_id": ObjectId(advert_id)},
        replacement={
            "title": title,
            "description": description,
            "flyer": upload_result["secure_url"],
            "category": category,
            "price": price,
            "advert_date": str(advert_date),
            "start_time": start_time.replace(tzinfo=None).isoformat(),
            "end_time": end_time.replace(tzinfo=None).isoformat()
        })

    return {"message": f"Advert {advert_id} updated successfully"}