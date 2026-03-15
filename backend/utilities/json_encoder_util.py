import json
import decimal
from datetime import datetime, date
from enum import Enum


class DateTimeJsonEncoder(json.JSONEncoder):
    """Date Time Encoder for JSON Data."""

    def default(self, obj):
        """Converts datetime to ISO format
        """
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()

        return super().default(obj)


class DecimalJsonEncoder(json.JSONEncoder):
    """Decimal Encoder for JSON Data."""

    def default(self, obj):
        """Converts decimal to string.
        """
        if isinstance(obj, decimal.Decimal):
            return str(obj)

        return super().default(obj)


class CustomJsonEncoder(json.JSONEncoder):
    """Date Time / Decimal Encoder for JSON Data."""

    def default(self, obj):
        """Converts decimal to string.
        """
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, Enum):
            return obj.name

        return super().default(obj)