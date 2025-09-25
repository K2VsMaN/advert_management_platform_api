# from fastapi import APIRouter, Depends
# from datetime import datetime, timezone, timedelta
# from pydantic import EmailStr
# from typing import Annotated
# from db import vendor_collection
# from fastapi import HTTPException, status
# from db import vendor_collection
# from fastapi import  Form
# import bcrypt
# import jwt
# import os


# vendors_router = APIRouter(tags=["Vendors"])

# @vendors_router.post("/vendors/register", summary="Register Vendor")
# def register_vendor(
#     vendor_name: Annotated[str, Form()],
#     email: Annotated[EmailStr, Form()],
#     password: Annotated[str, Form(min_length=8)]
# ):
#     vender_count = vendor_collection.count_documents(filter={"email": email})
#     if vender_count > 0:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vendor already exist")
    
#     hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
#     vendor_collection.insert_one({
#         "vendor_name": vendor_name,
#         "email": email,
#         "password": hashed_password
#     })
#     return {"message": "Vendor registered successfully!"}

# @vendors_router.post("/vendors/login", summary="Login Vendor")
# def login_vendor(
#     email: Annotated[EmailStr, Form()],
#     password: Annotated[str, Form()]
# ):
#     vendor_in_db = vendor_collection.find_one(filter={"email": email})
#     if not vendor_in_db:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email or password not found")
    
#     hashed_password_in_db = vendor_in_db["password"]

#     correct_password = bcrypt.checkpw(
#         password.encode("utf-8"),
#         hashed_password_in_db
#     )
#     if not correct_password:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password!")
#     encoded_jwt = jwt.encode(payload={
#         "id": str(vendor_in_db["_id"]),
#         "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60)
#    }, key=os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
#     return {"message": "Vendor logged in successfully!",
#             "access_token": encoded_jwt}