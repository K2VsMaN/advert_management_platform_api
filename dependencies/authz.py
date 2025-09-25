from dependencies.authn import authenticated_user
from fastapi import Depends, HTTPException, status
from typing import Annotated, Any


def has_role(role):
    def check_role(
            vendor: Annotated[Any, Depends(authenticated_user)]):
        if not vendor["role"] in role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access deneid!")
    return check_role