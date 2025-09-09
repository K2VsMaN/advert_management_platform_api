from fastapi import FastAPI, HTTPException, status
from bson.objectid import ObjectId
from db import adverts_collection

app = FastAPI()


@app.delete(
    "/adverts/{advert_id}",
    tags=["Delete"],
    summary="Delete an ad",
)
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

