def replace_advert_id(advert):
    advert["id"] = str(advert["_id"])
    del advert["_id"]
    return advert