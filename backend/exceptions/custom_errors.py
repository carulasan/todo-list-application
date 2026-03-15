class GenericApiV1Exception(Exception):
    def __init__(self, name: str):
        self.name = name


class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name
        self.message = f"{self.name} not found."

    def __str__(self):
        return self.message


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class DatabaseException(Exception):
    def __init__(self, info: str):
        super().__init__(info)
        self.name = info


class DatabaseConnectionError(Exception):
    def __init__(self, info: str):
        super().__init__(info)
        self.name = info


class DeletionForbiddenError(Exception):
    def __init__(self, error_code, parent_entity: str, child_entity: str):
        self.error_code = error_code
        self.message = f"Unable to delete the data. Please reassign any existing {child_entity} associated with the {parent_entity}."

    def __str__(self):
        return self.message

    def to_response(self) -> dict:
        """Returns a dictionary representation for a response."""
        return {"message": self.message, "error_code": self.error_code}


class FormValidationError(Exception):
    def __init__(
        self,
        message: str,
        error_code: int,
        errors: dict = None,
        transaction_id: str = None,
    ):
        """
        Custom exception for Form Validation Errors.

        Args:
            message (str): The error message.
            error_code (int): The error code.
            errors (None, optional): Additional details about the errors. Defaults to None.
        """
        self.message = message
        self.error_code = error_code
        self.errors = errors or {}
        self.transaction_id = transaction_id

    def __str__(self):
        combined_errors = self.message
        if self.errors and isinstance(self.errors, dict):
            for field, errors in self.errors.items():
                combined_errors = f"{combined_errors} " + ".".join(errors)

        return combined_errors

    def to_response(self) -> dict:
        """Returns a dictionary representation of the exception."""
        return {
            "message": self.message,
            "error_code": self.error_code,
            "errors": self.errors,
        }


class FormGenericError(Exception):
    def __init__(
        self,
        message: str,
        error_code: int,
        errors: dict = None,
        transaction_id: str = None,
    ):
        """
        Custom exception for Form Validation Errors.

        Args:
            message (str): The error message.
            error_code (int): The error code.
            errors (None, optional): Additional details about the errors. Defaults to None.
        """
        self.message = message
        self.error_code = error_code
        self.errors = errors or {}
        self.transaction_id = transaction_id

    def __str__(self):
        combined_errors = self.message
        if self.errors and isinstance(self.errors, dict):
            for field, errors in self.errors.items():
                combined_errors = f"{combined_errors} " + ".".join(errors)

        return combined_errors

    def to_response(self) -> dict:
        """Returns a dictionary representation of the exception."""
        return {
            "message": self.message,
            "error_code": self.error_code,
            "errors": self.errors,
        }


class FormSavingError(Exception):
    def __init__(
        self,
        message: str,
        details: str,
        error_code: int,
        transaction_id: str = None,
    ):
        """
        Custom exception for Form Saving Unexpected Error.

        Args:
            message (str): The error message.
            error_code (int): The error code.
            errors (None, optional): Additional details about the errors. Defaults to None.
        """
        self.message = message
        self.error_code = error_code
        self.details = details
        self.transaction_id = transaction_id

    def __str__(self):
        return self.message

    def to_response(self) -> dict:
        """Returns a dictionary representation of the exception."""
        return {
            "Message": self.message,
            "ErrorCode": self.error_code,
            "Details": self.details,
        }