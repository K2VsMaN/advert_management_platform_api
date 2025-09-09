from fastapi import FastAPI
from db import adverts_collection
from utils import replace_advert_id

    
app = FastAPI()


@app.get(
    "/adverts/",
    tags= ["Ads"],
    summary= "Get all adverts"
    )


def get_adverts():
    all_adverts = adverts_collection.find().to_list()
    return {"adverts": list(map(replace_advert_id, all_adverts))}