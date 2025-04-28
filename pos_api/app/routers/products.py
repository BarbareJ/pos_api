from fastapi import APIRouter, Depends

from app.dependencies import get_product_service
from app.schemas.products import (
    ProductCreate,
    ProductListResponse,
    ProductReadResponse,
    ProductUpdate,
)
from app.services.products import ProductService

router = APIRouter()


@router.post("", response_model=ProductReadResponse, status_code=201)
def create_product(
    data: ProductCreate, service: ProductService = Depends(get_product_service)
):
    product = service.create_product(data)
    return {"product": product}


@router.get("", response_model=ProductListResponse, status_code=200)
def list_products(service: ProductService = Depends(get_product_service)):
    products = service.list_products()
    return {"products": products}


@router.get("/{product_id}", response_model=ProductReadResponse, status_code=200)
def read_product(
    product_id: str, service: ProductService = Depends(get_product_service)
):
    product = service.get_product(product_id)
    return {"product": product}


@router.patch("/{product_id}", status_code=200)
def update_product_price(
    product_id: str,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    service.update_product(product_id, data)
    return {}
