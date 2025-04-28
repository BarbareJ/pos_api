from pydantic import BaseModel, Field


class UnitCreate(BaseModel):
    name: str = Field(..., example="კგ")


class UnitResponse(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class UnitReadResponse(BaseModel):
    unit: UnitResponse


class UnitListResponse(BaseModel):
    units: list[UnitResponse]
