from fastapi import FastAPI
from bson.objectid import ObjectId


app = FastAPI()


@app.delete(
    "/adverts/{advert_id}",
    tag= ["Delete"],
    summary= "Delete an ad",
    )
def delete_advert(advert_id: int):
    if not ObjectId.is_valid(advert_created):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")
    # Delete event from database
    delete_result =  events_collection.find_one_and_delete(filter={"_id": ObjectId(advert_created)})
    if not delete_result.deleted_count:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")