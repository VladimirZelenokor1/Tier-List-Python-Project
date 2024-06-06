from sqlalchemy import String, Column, Integer, ForeignKey, Table, BLOB
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


template_item = Table(
    'template_items',
    Base.metadata,
    Column('template_id', Integer, ForeignKey('templates.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    picture = Column(BLOB, nullable=False)


class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    picture = Column(BLOB, nullable=False)

    items = relationship('Item', secondary=template_item)


class TierList(Base):
    __tablename__ = "tier_lists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False)

    template = relationship("Template")
    items = relationship('TierListItem')


class TierListItem(Base):
    __tablename__ = "tier_list_items"
    tier_list_id = Column(Integer,
                          ForeignKey('tier_lists.id'),
                          nullable=False,
                          primary_key=True)
    item_id = Column(Integer,
                     ForeignKey('items.id'),
                     nullable=False,
                     primary_key=True)
    tier = Column(String, nullable=False)

    item = relationship("Item")
