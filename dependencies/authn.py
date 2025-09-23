import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from db import adverts_collection
from utils import replace_advert_id
from bson.objectid import ObjectId

def is_authenticated(
        authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    try:
        payload = jwt.decode(
            jwt=authorization.credentials,
            key= os.getenv("JWT_SECRET_KEY"),
            algorithms=os.getenv("JWT_ALGORITHM")
        )
        return payload["id"]
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
def authenticated_vendor(vendor_id: Annotated[str,Depends(is_authenticated)]):
    vendor = adverts_collection.find_one(filter={"id": ObjectId(vendor_id)})
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated vendor missing from database!"
        )
    return replace_advert_id(vendor)