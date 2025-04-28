# POS Service README

**A concise RESTful POS API** implemented with FastAPI and SQLite.

## User Stories

- **Cashier** opens and closes receipts.
- **Cashier** adds items to receipts.
- **Customer** views receipt details.
- **Manager** retrieves sales reports.

## Tech Stack & Quality

- **Framework:** FastAPI
- **Database:** SQLite
- **Linting:** ruff
- **Typing:** mypy
- **Testing:** pytest

## Endpoints

- **Units**
  - `POST /units`
  - `GET /units/{id}`
  - `GET /units`

- **Products**
  - `POST /products`
  - `GET /products/{id}`
  - `GET /products`
  - `PATCH /products/{id}`

- **Receipts**
  - `POST /receipts`
  - `POST /receipts/{id}/products`
  - `GET /receipts/{id}`
  - `PATCH /receipts/{id}` (close)
  - `DELETE /receipts/{id}`

- **Sales Report**
  - `GET /sales`


