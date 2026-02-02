from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    username: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
