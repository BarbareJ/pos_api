from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers import products, receipts, sales, units


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="POS System")

    app.include_router(units.router, prefix="/units", tags=["units"])
    app.include_router(products.router, prefix="/products", tags=["products"])
    app.include_router(receipts.router, prefix="/receipts", tags=["receipts"])
    app.include_router(sales.router, prefix="/sales", tags=["sales"])

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if isinstance(exc.detail, dict) and "message" in exc.detail:
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": {"message": exc.detail["message"]}},
            )
        return JSONResponse(
            status_code=exc.status_code, content={"error": {"message": str(exc.detail)}}
        )

    return app


app = create_app()
