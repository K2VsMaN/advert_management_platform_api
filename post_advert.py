from fastapi import  Form, File, UploadFile
from db import adverts_collection
from typing import Annotated
from datetime import date, time
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    )


def create_advert(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    category: Annotated[str, Form()],
    price: Annotated[float, Form()],
    advert_date: Annotated[date, Form(...)],
    start_time: Annotated[time, Form(...)],
    end_time: Annotated[time, Form(...)]):

    upload_result = cloudinary.uploader.upload(flyer.file)
    advert_created = {
        "title": title,
        "description": description,
        "flyer": upload_result["secure_url"],
        "category": category,
        "price": price,
        "advert_date": str(advert_date),
        "start_time": start_time.replace(tzinfo=None).isoformat(),
        "end_time": end_time.replace(tzinfo=None).isoformat()
    }
    
    advert_result = adverts_collection.insert_one(advert_created)

    return {
        "message": "Advert created successfully",
        "advert_id": str(advert_result.inserted_id)
        }