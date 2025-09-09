from fastapi import FastAPI,HTTPException, status

app = FastAPI()

@app.get(
    "/adverts/{advert_id}",
    tags= ["Adverts"],
    summary= "Get an advert detail by ID"
    )
def get_advert(advert_id: int):
    if advert_id not in advert_created:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Ad not found")
    return advert_created[advert_id]

