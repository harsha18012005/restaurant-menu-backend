from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: str

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    url: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True