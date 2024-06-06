from pydantic import ConfigDict, BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class ItemCreate(BaseModel):
    name: str
    description: str
    price: int
    picture: bytes


class Item(ItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TierListItem(BaseModel):
    item_id: int
    tier: str


class TemplateCreate(BaseModel):
    name: str
    picture: bytes
    items: list[int]


class Template(BaseModel):
    id: int
    name: str
    picture: bytes
    items: list[Item] = []
    model_config = ConfigDict(from_attributes=True)


class TierList(BaseModel):
    id: int
    template: Template
    items: list[TierListItem] = []
    model_config = ConfigDict(from_attributes=True)
