from fastapi import APIRouter
from db import adverts_collection
from utils import replace_advert_id
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from fastapi import  Form, File, UploadFile
from typing import Annotated
from datetime import date, time
import cloudinary.uploader



adverts_router = APIRouter(tags=["Adverts"])


@adverts_router.get(
    "/adverts/",
    summary="Get all adverts"
)
def get_adverts(
    title="",
    description="",
    limit=10,
    skip=0
):
    all_adverts = adverts_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()
    return {"adverts": list(map(replace_advert_id, all_adverts))}


@adverts_router.get("/adverts/{advert_id}")
def get_advert_by_id(advert_id):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    advert = adverts_collection.find_one({"_id": ObjectId(advert_id)})
    return {"data": replace_advert_id(advert)}


@adverts_router.post("/adverts")
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



@adverts_router.put("/adverts/{advert_id}")
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


@adverts_router.delete("/adverts/{advert_id}")
def delete_advert(advert_id):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    # Delete event from database
    delete_result = adverts_collection.delete_one(
        filter={"_id": ObjectId(advert_id)})
    if not delete_result:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    
    return {"message": f"Advert with id {advert_id} has been deleted successfully."}

