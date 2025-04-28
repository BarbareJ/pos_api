from fastapi import APIRouter, Depends

from app.dependencies import get_unit_service
from app.schemas.units import UnitCreate, UnitListResponse, UnitReadResponse
from app.services.units import UnitService

router = APIRouter()


@router.post("", response_model=UnitReadResponse, status_code=201)
def create_unit(
    data: UnitCreate,
    service: UnitService = Depends(get_unit_service),
):
    unit = service.create_unit(data)
    return {"unit": unit}


@router.get("", response_model=UnitListResponse, status_code=200)
def list_units(
    service: UnitService = Depends(get_unit_service),
):
    units = service.list_units()
    return {"units": units}


@router.get("/{unit_id}", response_model=UnitReadResponse, status_code=200)
def read_unit(
    unit_id: str,
    service: UnitService = Depends(get_unit_service),
):
    unit = service.get_unit(unit_id)
    return {"unit": unit}
