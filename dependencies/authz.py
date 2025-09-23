from dependencies.authn import authenticated_vendor
from fastapi import Depends, HTTPException, status
from typing import Annotated

permissions = [
    {
        "role": "vendor",
        "permission": ["post_advert", "get_adverts", "get_advert", "put_advert", "delete_advert"]
    },
    {
        "role": "user",
        "permission": ["get_adverts", "get_advert"]
    }
]

def has_role(role):
    def check_roles(
            vendor: Annotated[any, Depends(authenticated_vendor)]):
        if not vendor["role"] in role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access deneid!")
    return check_roles