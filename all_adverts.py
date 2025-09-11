from fastapi import FastAPI
from db import adverts_collection
from utils import replace_advert_id

    
app = FastAPI()


@app.get(
    "/adverts/",
    tags= ["Ads"],
    summary= "Get all adverts"
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