from fastapi import FastAPI, Form, File, UploadFile
from db import adverts_collection
from typing import Annotated

app = FastAPI()

@app.post("/adverts")
def create_advert(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    category: Annotated[str, Form()],
    price: Annotated[float, Form()]):

    advert_created = {
        "title": title,
        "description": description,
        "flyer": flyer.filename,
        "category": category,
        "price": price
    }

    advert_result = adverts_collection.insert_one(advert_created)

    return {
        "message": "Advert created successfully",
        "advert_id": str(advert_result.inserted_id)
        }