from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    unit_id: str
    name: str = Field(..., example="Apple")
    barcode: str = Field(..., example="1234567890")
    price: int = Field(..., example=520)


class ProductUpdate(BaseModel):
    price: int


class ProductResponse(BaseModel):
    id: str
    unit_id: str
    name: str
    barcode: str
    price: int

    class Config:
        orm_mode = True


class ProductReadResponse(BaseModel):
    product: ProductResponse


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
