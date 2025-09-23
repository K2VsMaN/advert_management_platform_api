from fastapi import HTTPException, status
from openai import OpenAI
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AdDescription(BaseModel):
    description: str

class AdCategory(BaseModel):
    category:str
    title: str

async def generate_related_adverts(ad: AdDescription):
    try:
        embedding = OpenAI.embeddings.create(
            model = "text-embedding-ada-002",
            input = ad.description
        )["data"][0]["embedding"]
        return {"related_ads": ["Ad #1", "Ad #2", "Ad #3"]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def price_suggestion(ad:AdCategory):
    base = 50 +len(ad.title.split()) * 5
    return {"suggested prices":f"${base} - ${base+30}"}