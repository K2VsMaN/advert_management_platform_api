from fastapi import APIRouter, Form
from db import users_collection
from utils import replace_user_id
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Annotated

users_router = APIRouter(tags=["Users"])

class UserDetails(BaseModel):
    username: str
    email: EmailStr
    password: str

@users_router.get(
    "/users/",
    summary="Get all users"
)
def get_users(
    username="",
    description="",
    limit=10,
    skip=0
):
    all_users = users_collection.find(
        filter={
            "$or": [
                {"username": {"$regex": username, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()
    return {"users": list(map(replace_user_id, all_users))}


@users_router.get("/users/{user_id}")
def get_user_by_id(user_id):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return {"data": replace_user_id(user)}


@users_router.post("/users")
def register_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()]):

    user_created = {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    
    registered_user = users_collection.insert_one(user_created)

    return {
        "message": "User registered successfully",
        "user_id": str(registered_user.inserted_id)
        }



# @users_router.put("/adverts/{advert_id}")
# def update_advert_by_id(
#         advert_id: str,
#         title: Annotated[str, Form()],
#         description: Annotated[str, Form()],
#         flyer: Annotated[UploadFile, File()],
#         category: Annotated[str, Form()],
#         price: Annotated[float, Form()],
#         advert_date: Annotated[date, Form(...)],
#         start_time: Annotated[time, Form(...)],
#         end_time: Annotated[time, Form(...)]):
#     if not ObjectId.is_valid(advert_id):
#         raise HTTPException(
#             status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid ID format")

#     upload_result = cloudinary.uploader.upload(flyer.file)
#     users_collection.replace_one(
#         filter={"_id": ObjectId(advert_id)},
#         replacement={
#             "title": title,
#             "description": description,
#             "flyer": upload_result["secure_url"],
#             "category": category,
#             "price": price,
#             "advert_date": str(advert_date),
#             "start_time": start_time.replace(tzinfo=None).isoformat(),
#             "end_time": end_time.replace(tzinfo=None).isoformat()
#         })

#     return {"message": f"Advert {advert_id} updated successfully"}


# @users_router.delete("/adverts/{advert_id}")
# def delete_advert(advert_id):
    if not ObjectId.is_valid(advert_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    # Delete event from database
    delete_result = users_collection.delete_one(
        filter={"_id": ObjectId(advert_id)})
    if not delete_result:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    
    return {"message": f"Advert with id {advert_id} has been deleted successfully."}