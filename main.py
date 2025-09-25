from fastapi import FastAPI 
import os
from dotenv import load_dotenv
import cloudinary
from routes.users import users_router
from routes.adverts import adverts_router
from routes.genai import genai_router

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

app.include_router(adverts_router, tags=["Adverts"])
app.include_router(users_router)
app.include_router(genai_router)
