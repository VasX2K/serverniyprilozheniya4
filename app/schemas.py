from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, confloat, conint, constr


class ProductCreate(BaseModel):
    title: constr(min_length=1, max_length=100)
    price: confloat(gt=0)
    count: conint(ge=0)
    description: constr(min_length=1, max_length=500)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: float
    count: int
    description: str


class ValidationProblem(BaseModel):
    location: str
    message: str
    error_type: str


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: list[ValidationProblem] = Field(default_factory=list)


class ValidatedUser(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class ValidatedUserResponse(BaseModel):
    username: str
    age: int
    email: EmailStr
    phone: str
    message: str


class UserIn(BaseModel):
    username: constr(min_length=1, max_length=80)
    age: conint(ge=0)


class UserOut(BaseModel):
    id: int
    username: str
    age: int
