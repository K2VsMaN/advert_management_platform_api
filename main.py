from fastapi import FastAPI
from post_advert import create_advert
from update_advert import update_advert_by_id
from all_adverts import get_adverts
from advert_details import get_advert_by_id
from delete import delete_advert

app = FastAPI(
    title="A Complete Advertisement Management Platform API",
    description="A basic backend for an e-commerce platform with product and order management."
)

app.get("/")
def get_home():
    return {"message": "Welcome to our Advert API"}

app.get("/adverts")(get_adverts)
app.get("/adverts/{advert_id}")(get_advert_by_id)
app.post("/adverts")(create_advert)
app.put("/adverts/{advert_id}")(update_advert_by_id)
app.delete("/adverts/{advert_id}")(delete_advert)
