from app.schemas import ValidationProblem


class CustomExceptionA(Exception):
    status_code = 400
    error_code = "custom_exception_a"

    def __init__(self, message: str = "CustomExceptionA was raised") -> None:
        self.message = message
        super().__init__(message)


class CustomExceptionB(Exception):
    status_code = 404
    error_code = "custom_exception_b"

    def __init__(self, message: str = "Requested resource was not found") -> None:
        self.message = message
        super().__init__(message)


def validation_problem_from_error(error: dict) -> ValidationProblem:
    location = ".".join(str(part) for part in error.get("loc", ()))
    return ValidationProblem(
        location=location,
        message=error.get("msg", "Invalid value"),
        error_type=error.get("type", "value_error"),
    )

