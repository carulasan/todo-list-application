import pytz
from datetime import datetime, timezone, timedelta, time, date
from typing import Optional
from zoneinfo import ZoneInfo
from app_logger import app_logger

UTC_TZ = pytz.utc
PH_TZ = pytz.timezone("Asia/Manila")
HOURS_DIFFERENCE = 8


class DateUtil:
    """Date Utility Helper."""

    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"

    DATETIME_FORMAT = "%Y-%m-%d"

    @staticmethod
    def get_last_date_of_month(year, month):
        """Returns the last date of the month.

        Args:
            year (int): Year, i.e. 2022
            month (int): Month, i.e. 1 for January

        Returns:
            date (datetime): Last date of the current month
        """

        if month == 12:
            last_date = datetime(year, month, 31, 23, 59, 59)
        else:
            last_date = datetime(year, month + 1, 1, 23, 59, 59) + timedelta(days=-1)

        return last_date

    @staticmethod
    def convert_utc_to_ph_datetime(datetime_value):
        """Converts UTC+0 to Philippine UTC+8 Datetime Value.
        This adds additional 8 hours to the given datetime.

        Args:
            datetime_value (datetime): Date & Time Value in UTC+0

        Returns:
            datetime
        """
        return datetime_value.astimezone(PH_TZ)

    @staticmethod
    def recognize_naive_datetime_as_pht(datetime_value):
        """Recognizes Naive Datetime as Philippine Time.

        Args:
            datetime_value (datetime): Date & Time Value.

        Returns:
            datetime
        """
        return datetime_value.replace(tzinfo=ZoneInfo("Asia/Manila"))

    @staticmethod
    def recognize_datetime_utc_to_ph_timezone(datetime_value):
        """Recognizes Datetime UTC+0 as Philippine UTC+8.
        This removes the +8 hours added to the UTC datetime when converted as Local Timezone.

        Args:
            datetime_value (datetime): Date & Time Value in UTC+0

        Returns:
            datetime: UTC+8
        """
        local_datetime = datetime_value.astimezone(PH_TZ)

        return local_datetime + timedelta(hours=-8)
    
    @staticmethod
    def datetime_minus_hours_difference(datetime_value: datetime) -> datetime:
        """
        Subtracts a predefined number of hours from the given datetime value.

        Args:
            datetime_value (datetime): The original datetime value.

        Returns:
            datetime: A new datetime value with HOURS_DIFFERENCE subtracted.
            
        Example:
            Input: 
                2025-11-17 16:08:00
                
            Output: 
                16:08:00+00:00
        """
        
        return datetime_value - timedelta(hours=HOURS_DIFFERENCE)

    @staticmethod
    def convert_str_to_datetime(
        datetime_str: str, datetime_format: Optional[str] = None
    ) -> Optional[datetime]:
        """Converts String Datetime to Datetime Object.

        Args:
            datetime_str (str): Datetime value.
            datetime_format (Optional[str]): Datetime expected format. Defaults to None.

        Returns:
            Optional[str]
        """
        if not datetime_str:
            return datetime_str

        if not datetime_format:
            datetime_format = DateUtil.DEFAULT_DATETIME_FORMAT

        return datetime.strptime(datetime_str, datetime_format)

    @staticmethod
    def convert_datetime_to_str(
        datetime_val: datetime, datetime_format: Optional[str] = None
    ) -> Optional[str]:
        """Converts Datetime Object to Datetime String.

        Args:
            datetime_val (datetime): Datetime object.
            datetime_format (Optional[str]): Datetime output format. Defaults to None.

        Returns:
            Optional[str]:
        """
        if not datetime_val:
            return datetime_val

        if not datetime_format:
            datetime_format = DateUtil.DEFAULT_DATETIME_FORMAT

        return datetime_val.strftime(datetime_format)

    @staticmethod
    def convert_datetime_to_str_date_only(
        datetime_val: datetime, datetime_format: Optional[str] = None
    ) -> Optional[str]:
        """Converts Datetime Object to Datetime String.

        Args:
            datetime_val (datetime): Datetime object.
            datetime_format (Optional[str]): Datetime output format. Defaults to None.

        Returns:
            Optional[str]:
        """
        if not datetime_val:
            return datetime_val

        if not datetime_format:
            datetime_format = DateUtil.DATETIME_FORMAT

        return datetime_val.strftime(datetime_format)

    @staticmethod
    def is_datetime_earlier_than_now(
        datetime_value: datetime, is_asia_timezone: bool = True
    ) -> bool:
        """Checks if given Date & Time value is earlier than Current Date & Time.

        Args:
            datetime_value (datetime): _description_
            is_asia_timezone (bool, optional): _description_. Defaults to True.

        Returns:
            bool
        """
        try:
            # UAT uses PH timestamp in DB
            # Production uses UTC timestamp in DB
            if is_asia_timezone:
                current_time = datetime.now(PH_TZ)
                datetime_value = datetime_value.replace(tzinfo=PH_TZ)
            else:
                current_time = datetime.now(timezone.utc)
                datetime_value = datetime_value.replace(tzinfo=UTC_TZ)

            # print(f"Compare Current DT: {current_time} < {datetime_value}")
            return current_time > datetime_value
        except Exception as e:
            print(f"Compare Current DT: {current_time} < {datetime_value}. Error: {e}")
            return False

    @staticmethod
    def get_current_local_datetime() -> datetime:
        """Retrieves current local date & time or Philippine time."""
        return datetime.now(PH_TZ)

    @staticmethod
    def convert_ph_to_utc_datetime(datetime_value):
        """Converts Philippine UTC+8 to UTC+0 Datetime Value.
        Lessen current time with 8 hours.

        Args:
            datetime_value (datetime): Date & Time Value in UTC+0

        Returns:
            datetime
        """
        return datetime_value.astimezone(UTC_TZ)

    @staticmethod
    def display_datetime_remove_milliseconds(date_time: any) -> datetime:
        """Removes milliseconds from datetime value.

        Args:
            date_time (datetime): Datetime value.

        Returns:
            datetime
        """

        if date_time is None:
            return date_time

        if type(date_time) is str:
            date_time = DateUtil.convert_str_to_datetime(date_time)
        return date_time.replace(microsecond=0)

    @staticmethod
    def converts_date_to_datetime(
        date_value: date, hour: int = 0, minute: int = 0, second: int = 0
    ) -> datetime:
        """Converts date to datetime.

        Args:
            date_value (date): Date value.
            hour (int, optional): Hour. Defaults to 0.
            minute (int, optional): Minute. Defaults to 0.
            second (int, optional): Second. Defaults to 0.

        Returns:
            datetime
        """
        if isinstance(date_value, datetime):
            return date_value

        if not isinstance(date_value, date):
            raise ValueError("Invalid date.")

        return datetime.combine(
            date_value, time(hour=hour, minute=minute, second=second)
        )

    @staticmethod
    def display_datetime_format(date_value: datetime):
        """
        Display default datetime format

        @params:
            date_value(datetime):
        @returns:
            str: "2025-06-17 04:11:11"
        """
        return date_value.strftime(DateUtil.DEFAULT_DATETIME_FORMAT)
    

    @staticmethod
    def is_expired_against_utc(datetime_value: datetime) -> bool:
        """
        Checks if the given datetime (in any timezone) has already passed 
        compared to the current UTC time.

        Args:
            datetime_value (datetime): Datetime to compare, should be aware (timezone-aware).

        Returns:
            bool: True if datetime is in the past (expired), False otherwise.
        """
        if datetime_value.tzinfo is None:
            raise ValueError("Provided datetime must be timezone-aware.")

        now_utc = datetime.now(timezone.utc)
        return now_utc >= datetime_value.astimezone(timezone.utc)

    @staticmethod
    def convert_utc_to_pht(date_to_convert: datetime):
        """ Convert UTC datetime to PH time (formatted) """
        try:
            if not date_to_convert:
                return None
        
            date_to_convert = date_to_convert.astimezone(PH_TZ)
            return date_to_convert
        except Exception as e:
          app_logger.error(f"DateUtil.convert_utc_to_pht | date_to_convert={date_to_convert} | Exception occur={e}")
          return None
    
    @staticmethod
    def to_d_prefix_timestamp(date_time: datetime) -> str:
        if isinstance(date_time, datetime):
            return f"$D_{int(date_time.timestamp())}"
        return None
        
    @staticmethod
    def get_seconds_until_midnight():
        now = datetime.now()
        now = now.astimezone(PH_TZ)
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = int((midnight - now).total_seconds())

        """Returns the number of seconds until midnight.
        """
        return seconds_until_midnight
