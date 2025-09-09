from fastapi import FastAPI, Form, File, UploadFile

    
app = FastAPI(
    title="A Complete Advertisement Management Platform API",
    description="A basic backend for an e-commerce platform with product and order management."
    )


@app.get(
    "/adverts/",
    tags= ["Ads"],
    summary= "Get all adverts"
    )
def get_adverts():
    return list(advert_created)