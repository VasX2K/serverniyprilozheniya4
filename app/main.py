from itertools import count
from threading import Lock

from fastapi import Depends, FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import CustomExceptionA, CustomExceptionB, validation_problem_from_error
from app.models import Product
from app.schemas import (
    ErrorResponse,
    ProductCreate,
    ProductRead,
    UserIn,
    UserOut,
    ValidatedUser,
    ValidatedUserResponse,
)


app = FastAPI(title="KR4 FastAPI Application", version="1.0.0")

users_db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


def reset_user_store() -> None:
    global _id_seq
    with _id_lock:
        users_db.clear()
        _id_seq = count(start=1)


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(_, exc: CustomExceptionA) -> JSONResponse:
    print(f"CustomExceptionA: {exc.message}")
    payload = ErrorResponse(error_code=exc.error_code, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(_, exc: CustomExceptionB) -> JSONResponse:
    print(f"CustomExceptionB: {exc.message}")
    payload = ErrorResponse(error_code=exc.error_code, message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    problems = [validation_problem_from_error(error) for error in exc.errors()]
    payload = ErrorResponse(
        error_code="validation_error",
        message="Request validation failed",
        details=problems,
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "message": "KR4 FastAPI application is running"}


@app.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.id)))


@app.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    created_product = Product(**product.model_dump())
    db.add(created_product)
    db.commit()
    db.refresh(created_product)
    return created_product


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise CustomExceptionB(f"Product with id={product_id} was not found")
    return product


@app.get("/demo-errors/a", response_model=dict)
def raise_custom_exception_a() -> dict:
    raise CustomExceptionA("Business rule failed for demo endpoint A")


@app.get("/demo-errors/b", response_model=dict)
def raise_custom_exception_b() -> dict:
    raise CustomExceptionB("Demo resource was not found")


@app.post("/validate-user", response_model=ValidatedUserResponse)
def validate_user(user: ValidatedUser) -> ValidatedUserResponse:
    return ValidatedUserResponse(
        username=user.username,
        age=user.age,
        email=user.email,
        phone=user.phone or "Unknown",
        message="User data is valid",
    )


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn) -> dict:
    user_id = next_user_id()
    users_db[user_id] = user.model_dump()
    return {"id": user_id, **users_db[user_id]}


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> dict:
    if user_id not in users_db:
        raise CustomExceptionB("User not found")
    return {"id": user_id, **users_db[user_id]}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> Response:
    if users_db.pop(user_id, None) is None:
        raise CustomExceptionB("User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
