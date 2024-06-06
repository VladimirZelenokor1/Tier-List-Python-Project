from typing import Optional

from sqlalchemy import and_, BLOB
from sqlalchemy.orm import Session

from models import (
    TierList,
    TierListItem,
    User,
    Template,
    Item
)
from db import DBContext
from schemas import UserCreate
from security import hash_password, manager


@manager.user_loader()
def get_user(email: str, db: Session = None) -> Optional[User]:
    """Return the user with the corresponding email"""
    if db is None:
        with DBContext() as db:
            return db.query(User).filter(User.email == email).first()
    else:
        return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new entry in the database user table"""
    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_template(name: str,
                    items: list[int],
                    picture: BLOB,
                    db: Session) -> Template:
    items = db.query(Item).where(Item.id.in_(items))
    template = Template(name=name, picture=picture)
    [template.items.append(i) for i in items]
    db.add(template)
    db.commit()
    return template


def get_all_templates(db: Session) -> list[Template]:
    return db.query(Template).all()


def get_template(template_id: int, db: Session) -> Template:
    return db.query(Template).filter_by(id=template_id).first()


def create_item(name: str,
                description: str,
                price: int,
                picture: BLOB,
                db: Session) -> Item:
    item = Item(name=name,
                description=description,
                price=price,
                picture=picture)
    db.add(item)
    db.commit()
    return item


def get_tierlist_item(item_id: int, tier_list_id: int, db: Session) -> (
        TierListItem):
    return db.query(TierListItem).filter(
        and_(TierListItem.item_id == item_id,
             TierListItem.tier_list_id == tier_list_id)).first()


def rank_tierlist_item(item_id: int,
                       tier_list_id: int,
                       tier: str,
                       db: Session) -> TierListItem:
    item = get_tierlist_item(item_id, tier_list_id, db)
    if item:
        item.tier = tier
    else:
        item = TierListItem(item_id=item_id,
                            tier_list_id=tier_list_id,
                            tier=tier)
    db.add(item)
    db.commit()
    return item


def delete_tierlist_item(item_id: int,
                         tier_list_id: int,
                         db: Session) -> None:
    item = get_tierlist_item(item_id, tier_list_id, db)
    if item:
        db.delete(item)
        db.commit()


def get_item(item_id: int, db: Session) -> Item:
    return db.query(Item).filter_by(id=item_id).first()


def get_all_tierlists(user_id: int, db: Session) -> list[TierList]:
    return db.query(TierList).filter_by(user_id=user_id).all()


def get_tierlist(template_id: int, user_id: int, db: Session) -> Item:
    return db.query(TierList).filter(
        and_(TierList.template_id == template_id,
             TierList.user_id == user_id)).first()


def get_tierlist_by_id(tierlist_id: int, db: Session) -> Item:
    return db.query(TierList).filter_by(id=tierlist_id).first()


def create_tierlist(template_id: int, user_id: int, db: Session) -> TierList:
    tierlist = TierList(template_id=template_id, user_id=user_id)
    db.add(tierlist)
    db.commit()
    return tierlist
