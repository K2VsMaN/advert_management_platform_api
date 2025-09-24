from fastapi import FastAPI 
import os
from dotenv import load_dotenv
import cloudinary
from routes.users import users_router
from routes.adverts import adverts_router

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    )

app = FastAPI(
    title="A Complete Advertisement Management Platform API",
    description="A basic backend for an e-commerce platform with product and order management."
)


@app.get("/")
def get_home():
    return {"message": "Welcome to our Advert API"}

<<<<<<< HEAD



app.get("/adverts")(get_adverts)
app.get("/adverts/{advert_id}")(get_advert_by_id)
app.post("/adverts")(create_advert)
app.put("/adverts/{advert_id}")(update_advert_by_id)
app.delete("/adverts/{advert_id}")(delete_advert)
=======
app.include_router(adverts_router)
app.include_router(users_router)
>>>>>>> 033cd5429d348dd1ffcf281e3a856db807f43921
