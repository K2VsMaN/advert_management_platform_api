from fastapi import APIRouter, Depends
from db import adverts_collection
from utils import replace_advert_id, genai_client
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from fastapi import Form, File
from typing import Annotated
from datetime import date, time
import cloudinary.uploader
from dependencies.authn import is_authenticated
from dependencies.authz import has_role
from google.genai import types


adverts_router = APIRouter()


@adverts_router.get(
    "/adverts",
    summary="Get all adverts"
)
def get_adverts(
    title="",
    description="",
    category="",
    limit=10,
    skip=0
):
    all_adverts = adverts_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
                {"category": {"$regex": category, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()
    return {"adverts": list(map(replace_advert_id, all_adverts))}


@adverts_router.get("/adverts/{advert_id}", summary="Get advert by ID")
def get_advert_by_id(advert_id):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")
    advert = adverts_collection.find_one({"_id": ObjectId(advert_id)})
    return {"data": replace_advert_id(advert)}


@adverts_router.get("/adverts/{advert_id}/related_adverts")
def get_related_adverts(advert_id, limit=10, skip=0):
    # Check if advert id is valid
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received!")
    # Get all adverts from database by id
    advert = adverts_collection.find_one({"_id": ObjectId(advert_id)})
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Advert not found!")
    # Get similar advert in the database
    similar_adverts = adverts_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": advert["title"], "$options": "i"}},
                {"description": {
                    "$regex": advert["description"], "$options": "i"}},
                {"category": {"$regex": advert["category"], "$options": "i"}}
            ]},
        limit=int(limit),
        skip=int(skip)
    ).to_list()
    # Return response
    return {"data": list(map(replace_advert_id, similar_adverts))}


@adverts_router.get("/adverts/vendor/me", tags=["Vendor Dashboard"], dependencies=[Depends(has_role("vendor"))])
def get_my_adverts(vendor_id: Annotated[str, Depends(is_authenticated)]):
    # Use the vendorID string dirctly in the database query.
    adverts_cursor = adverts_collection.find(filter={"owner": vendor_id})

    advert_list = list(adverts_cursor)

    # Return response, ensuring MongoDB's _id is handled if necessary
    return {"data": list(map(replace_advert_id, advert_list))}


@adverts_router.post("/adverts", summary="Add a new advert", dependencies=[Depends(has_role("vendor"))])
def create_advert(
    title: Annotated[str, Form()],
    category: Annotated[str, Form()],
    location: Annotated[str, Form()],
    price: Annotated[float, Form()],
    advert_date: Annotated[date, Form(...)],
    start_time: Annotated[time, Form(...)],
    end_time: Annotated[time, Form(...)],
    vendor_id: Annotated[str, Depends(is_authenticated)],
    description: Annotated[str, Form()] = None,
    flyer: Annotated[bytes, File()] = None,
):
    # Ensure an advert with title and vendor_id combined does not exist
    advert_count = adverts_collection.count_documents(filter={"$and": [
        {"title": title},
        {"owner": vendor_id}
    ]})
    if advert_count > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Advert with title: {title} and vendor_id: {vendor_id} already exist!")

    if not flyer:
        # Generate AI image with Gemini
        response = genai_client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=title,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        flyer = response.generated_images[0].image.image_bytes

    upload_result = cloudinary.uploader.upload(flyer)
    advert_created = {
        "title": title,
        "description": description,
        "location": location,
        "flyer": upload_result["secure_url"],
        "category": category,
        "price": price,
        "advert_date": str(advert_date),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "owner": vendor_id
    }

    advert_result = adverts_collection.insert_one(advert_created)

    return {
        "message": "Advert created successfully",
        "advert_id": str(advert_result.inserted_id),
    }


@adverts_router.put("/adverts/{advert_id}", summary="Update an advert", dependencies=[Depends(has_role("vendor"))])
def update_advert_by_id(
        advert_id: str,
        title: Annotated[str, Form()],
        category: Annotated[str, Form()],
        location: Annotated[str, Form()],
        price: Annotated[float, Form()],
        advert_date: Annotated[date, Form(...)],
        start_time: Annotated[time, Form(...)],
        end_time: Annotated[time, Form(...)],
        vendor_id: Annotated[str, Depends(is_authenticated)],
        description: Annotated[str, Form()] = None,
        flyer: Annotated[bytes, File()] = None,
):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid ID format")

    if not flyer:
        # Generate AI image with Gemini
        response = genai_client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=title,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        flyer = response.generated_images[0].image.image_bytes

    upload_result = cloudinary.uploader.upload(flyer)
    replace_result = adverts_collection.replace_one(
        filter={"_id": ObjectId(advert_id), "owner": vendor_id},
        replacement={
            "title": title,
            "description": description,
            "location": location,
            "flyer": upload_result["secure_url"],
            "category": category,
            "price": price,
            "advert_date": str(advert_date),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "owner": vendor_id
        })
    if not replace_result.modified_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No advert found to replace!")
    return {"message": f"Advert {advert_id} updated successfully"}


@adverts_router.delete("/adverts/{advert_id}", summary="Delete an advert", dependencies=[Depends(has_role("vendor"))])
def delete_advert(advert_id, vendor_id: Annotated[str, Depends(is_authenticated)]):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    # Delete advert from database
    delete_result = adverts_collection.delete_one(
        filter={"_id": ObjectId(advert_id), "owner": vendor_id})
    if not delete_result:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")

    return {"message": f"Advert with id {advert_id} has been deleted successfully."}
