from fastapi import Depends, APIRouter, HTTPException

import requests

import db_actions
from db import get_db
from schemas import (
    TierList,
    Template,
    Item,
    ItemCreate,
    TemplateCreate
)
from security import manager


service_router = APIRouter()


@service_router.get("/template/all", response_model=list[Template])
def get_all_templates(db=Depends(get_db)):
    return db_actions.get_all_templates(db)


@service_router.get("/template/get/{template_id}",
                    response_model=Template)
def get_template(template_id: int, db=Depends(get_db)):
    result = db_actions.get_template(template_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The template with this id does not exist.")


@service_router.post("/template/create", response_model=Template)
def create_template(template: TemplateCreate,
                    user=Depends(manager),
                    db=Depends(get_db)):
    template = db_actions.create_template(template.name,
                                          template.items,
                                          template.picture, db)
    return Template.from_orm(template)


@service_router.get("/item/get/{item_id}", response_model=Item)
def get_item(item_id: int, db=Depends(get_db)):
    result = db_actions.get_item(item_id, db)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The item with this id does not exist.")


@service_router.post("/item/create", response_model=Item)
def create_item(item: ItemCreate, user=Depends(manager), db=Depends(get_db)):
    item = db_actions.create_item(item.name,
                                  item.description,
                                  item.price,
                                  item.picture,
                                  db)
    return Item.from_orm(item)


@service_router.post("/item/rank/")
def rank_item(item_id: int,
              tierlist_id: int,
              tier: str,
              user=Depends(manager),
              db=Depends(get_db)):
    item = db_actions.get_item(item_id, db)
    if not item:
        raise HTTPException(status_code=404,
                            detail="The item with this id does not exist.")

    tierlist = db_actions.get_tierlist_by_id(tierlist_id, db)
    if not tierlist:
        raise HTTPException(status_code=404,
                            detail="The tierlist for this "
                                   "template and user does not exist.")

    if tier not in "ABCDEFS_":
        raise HTTPException(status_code=422,
                            detail="Invalid data for rank was provided.")

    if tier == "_":
        db_actions.delete_tierlist_item(item_id, tierlist.id, db)
        return {'status_code': 200, 'detail': 'The item unranked.'}
    else:
        item = db_actions.rank_tierlist_item(item_id, tierlist.id, tier, db)
        return {'status_code': 200, 'detail': f"The item was ranked with "
                                              f"{item.tier} tier."}


@service_router.get("/tierlist/all", response_model=list[TierList])
def get_all_tierlists(user=Depends(manager), db=Depends(get_db)):
    return db_actions.get_all_tierlists(user.id, db)


@service_router.get("/tierlist/get/{template_id}", response_model=TierList)
def get_tierlist(template_id: int, user=Depends(manager), db=Depends(get_db)):
    _tierlist = db_actions.get_tierlist(template_id, user.id, db)

    if _tierlist:
        return _tierlist

    new_tierlist = db_actions.create_tierlist(template_id, user.id, db)
    return TierList.from_orm(new_tierlist)


@service_router.get("/fact")
def get_fact():
    url = f"https://uselessfacts.jsph.pl/api/v2/facts/today?language={'en'}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["text"]
    else:
        return "Failed to fetch today's useless fact"
