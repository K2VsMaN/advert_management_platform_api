from fastapi import HTTPException, Form, File, UploadFile, status
from db import adverts_collection
from bson.objectid import ObjectId
from typing import Annotated
import cloudinary
import cloudinary.uploader
from datetime import date, time
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    )

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
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid ID format")

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
