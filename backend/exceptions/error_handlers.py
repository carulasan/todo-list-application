import json
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app_logger import app_logger as logger
from utilities.string_util import to_pascal_case

OLD_PUBLIC_ENDPOINT_PREFIX = "/api/v1/public/"


def get_custom_error_message(error_type, error_params):
    """Retrieves custom error message based on error type."""
    custom_errors = {
        "json_invalid": "The request format is not valid",
        "missing": "This field is required.",
        "int_type": "This field value must be an integer.",
        "int_parsing": "This field value must be a valid integer.",
        "string_type": "This field value must be a string.",
        "string_too_short": "This field value must have at least {{value}} characters.",
        "string_too_long": "This field value must have at most {{value}} characters.",
        "less_than": "This field value must be less than {{value}}.",
        "less_than_equal": "This field value must be less than or equal to {{value}}.",
        "greater_than": "This field value must greater than {{value}}.",
        "greater_than_equal": "This field value must greater than or equal to {{value}}.",
        "date_from_datetime_parsing": "This field date format is not valid.",
        "date_type": "This field date format is not valid.",
        "too_short": "Ensure this value has at least {{value}} items.",
        "value_error": "{{value}}",
    }

    message = custom_errors.get(error_type)

    if not message or "{{value}}" not in message:
        return message

    # Replace message dynamic values
    match error_type:
        case "string_too_short":
            message = message.replace(
                "{{value}}", str(error_params.get("min_length", 0))
            )
        case "string_too_long":
            message = message.replace(
                "{{value}}", str(error_params.get("max_length", 0))
            )
        case "less_than":
            message = message.replace("{{value}}", str(error_params.get("lt", 0)))
        case "less_than_equal":
            message = message.replace("{{value}}", str(error_params.get("le", 0)))
        case "greater_than":
            message = message.replace("{{value}}", str(error_params.get("gt", 0)))
        case "greater_than_equal":
            message = message.replace("{{value}}", str(error_params.get("ge", 0)))
        case "too_short":
            message = message.replace("{{value}}", str(error_params.get("min_length", 0)))

        # Custom raised value errors
        case "value_error":
            current_message = str(error_params.get("error"))

            if current_message == "None":
                current_message = str(error_params.get("reason"))

            new_message = (
                current_message.replace("Value error, ", "")
                if current_message
                else current_message
            )
            message = message.replace("{{value}}", new_message)
        case _:
            # Default case for any unmatched error_type
            pass

    return message


def format_validation_error(exc):
    """Format validation exception messages.
    Original Errors Messages:
        - missing: Field required
        - string_type: Input should be a valid string
        - int_parsing: Input should be a valid integer, unable to parse string as an integer
        - string_too_long: String should have at most 150 characters
        - string_too_short: String should have at least 10 characters.
        - less_than_equal: Input should be less than or equal to 1000
        - greater_than_equal: Input should be greater than or equal to 1
        - greater_than: Input should be greater than 1
        - less_than: Input should be less than 1
        - json_invalid: JSON decode error
        - date_from_datetime_parsing: Input should be a valid date or datetime, invalid character in year

    Args:
        Exception

    Returns:
        dict: Validation errors
    """
    validation_errors = {}

    for error in exc.errors():
        loc = error.get("loc")
        message = error.get("msg")

        if not loc or not isinstance(loc, tuple):
            continue

        # Custom Error Handler

        error_type = error.get("type")
        error_params = error.get("ctx", dict())

        custom_msg = get_custom_error_message(error_type, error_params)

        if custom_msg:
            message = custom_msg
        else:
            print("Not Customized Field Error: ", error_type, error_params, error)

        key = loc[-1]
        if isinstance(key, int):
            key = "Body"

        validation_errors[key] = [message]

    return validation_errors


def format_error_response_based_on_route(request: Request, response_data) -> dict:
    """Formats error response message based on current route.
    Special formatting is needed to mimic old API (Zeus SC)'s response
    """
    current_route = request.url.path

    # Backwards compatibility for Zeus SC same response
    if current_route.startswith(OLD_PUBLIC_ENDPOINT_PREFIX):
        return {to_pascal_case(key): value for key, value in response_data.items()}

    return response_data


async def handle_unauthorized_exception(request: Request, exception_info):
    """Unauthorized Exception Handler."""
    error_data = {
        "message": "The authentication credentials are either missing or invalid."
    }
    result = format_error_response_based_on_route(request, error_data)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(result),
    )


async def handle_forbidden_exception(request: Request, exception_info):
    """Forbidden Exception Handler."""
    error_data = {"message": "You do not have permission to perform this action."}
    result = format_error_response_based_on_route(request, error_data)

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder(result),
    )


async def handle_http_403_exception(request: Request, exception_info):
    """HTTP 403 Forbidden Exception Handler."""
    if exception_info.status_code == status.HTTP_403_FORBIDDEN:
        error_data = {"message": "You do not have permission to perform this action."}
        result = format_error_response_based_on_route(request, error_data)

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder(result),
        )
    return await request.app.default_exception_handler(request, exception_info)


async def handle_not_found_exception(request: Request, exception_info):
    """Not Found Exception Handler."""
    error_data = {"message": exception_info.message}
    result = format_error_response_based_on_route(request, error_data)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(result),
    )


async def handle_generic_exception(request: Request, exc):
    """Generic Exception Handler."""
    error_data = {"message": "Internal Server Error"}
    result = format_error_response_based_on_route(request, error_data)
    logger.error(f"Generic Exception: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(result),
    )


async def handle_validation_exception(request: Request, exc):
    """Request and Validation Exception Handler."""
    validation_errors = format_validation_error(exc)

    try:
        transaction_id = request.state.transaction_uuid
    except AttributeError:
        transaction_id = None

    logger.error(
        str(
            {
                "transaction_id": transaction_id,
                "path": request.url.path,
                "query_params": request.query_params,
                "errors": validation_errors,
            }
        )
    )

    error_data = {"message": "Invalid Request.", "errors": validation_errors}
    response_content = format_error_response_based_on_route(request, error_data)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response_content
    )


async def handle_deletion_forbidden_exception(request: Request, exception_info):
    """Deletion Forbidden Exception Handler."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(exception_info.to_response()),
    )


async def handle_form_validation_exception(request: Request, exception_info):
    """Form Validation Exception Handler."""

    errors = exception_info.to_response()
    log_error = {
        "error_type": "form_validation",
        "transaction_id": exception_info.transaction_id,
        "details": errors,
    }
    logger.error(f"{json.dumps(log_error)}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(errors),
    )