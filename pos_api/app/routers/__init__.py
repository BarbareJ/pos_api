from .products import router as products_router
from .receipts import router as receipts_router
from .sales import router as sales_router
from .units import router as units_router

__all__ = [
    "units_router",
    "products_router",
    "receipts_router",
    "sales_router",
]
