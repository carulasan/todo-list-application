import logging
import redis
from typing import Optional

from settings import db_settings
from app_logger import app_logger

class RedisCacheClient():
    """Redis Cache Client Connection."""

    client = None
    connected = False

    def __init__(self, cache_uri, logger=logging.Logger) -> None:
        self.cache_uri = cache_uri
        self.logger = logger

    def open(self) -> None:
        """Opens Redis Client Connection."""
        try:
            self.client = redis.from_url(
                self.cache_uri,
                socket_timeout=5,  # Timeout for socket reads and writes in seconds
                socket_connect_timeout=5,  # Timeout for establishing the initial connection in seconds
                retry_on_timeout=False,  # If set to True, Redis will retry on timeout
                max_connections=10,  # Maximum number of connections in the connection pool
            )
            self.connected = True
            self.logger.info(f"Redis connection is established. DB: {self.cache_uri}")
        except redis.AuthenticationError:
            self.logger.error("Redis Authentication Error")
            self.connected = False
        except redis.exceptions.TimeoutError as e:
            self.logger.error(f"Redis Timeout Error: {e}")
        except Exception as e:
            self.logger.error(f"Redis Connection Error: {e}")
            self.connected = False

    def connection(self) -> None:
        """Retrieves Redis Client Connection."""
        if not self.is_connected():
            raise ValueError("Redis connection is not established.")

        return self.client

    def close(self) -> None:
        """Closes Redis Client Connection."""
        if not self.is_connected():
            raise ValueError("Redis connection is not established.")

        self.client.close()

    def is_connected(self) -> bool:
        """Checks if Redis connection is established.

        Returns:
            bool
        """
        return self.connected

    def get_data(self, key: str):
        """Retrieves cache data.

        Args:
            key (str): Cache key.

        Returns:
            str: Cache data.
        """
        cache_result = None
        try:
            cache_result = self.client.get(key)
            self.logger.info(f"Retrieved cache key: {key} value")
        except redis.exceptions.TimeoutError:
            self.logger.error("Redis get operation timed out.")
        except Exception as e:
            self.logger.error(f"Failed to get cache key: {key} due to Error: {e}")

        return cache_result

    def set_data(self, key: str, value: any, expiry: Optional[int] = 604800):
        """Sets cache data.

        Args:
            key (str): Cache key.
            value (str, int): Cache value.
            expiry (int, optional): Cache expiration in seconds. Defaults to 86048006400.

        Returns:
            _type_: _description_
        """
        is_updated = None
        try:
            is_updated = self.client.set(key, value, expiry)
            if value is not None:
                self.logger.info(
                    f"Updated cache key: {key} value to: " + str(value)[:100]
                )
        except redis.exceptions.TimeoutError:
            self.logger.error("Redis set operation timed out.")
        except Exception as e:
            self.logger.error(
                f"Failed to set cache key: {key} value to: {value} due to Error: {e}"
            )

        return is_updated

    def delete_data(self, key: str):
        """Deletes cache data.

        Args:
            key (str): Cache key.

        Returns:
            any
        """
        cache_result = None
        if not self.client:
            self.logger.info(
                f"Failed to delete cache key: {key} due to redis connection."
            )
            return cache_result

        try:
            cache_result = self.client.delete(key)
            self.logger.info(f"Delete cache key: {key} - {cache_result}")
        except redis.exceptions.TimeoutError:
            self.logger.error("Redis delete operation timed out.")
        except Exception as e:
            self.logger.error(f"Failed to delete cache key: {key} due to Error: {e}")

        return cache_result

    def delete_data_with_wildcard(self, key_pattern: str) -> bool:
        """Deletes cache data (supports wildcards).

        Args:
            key_pattern (str): Cache key or pattern (e.g. 'user:*').

        Returns:
            bool: True if at least one key was deleted, False otherwise.
        """
        if not self.client:
            self.logger.info(
                f"Failed to delete cache key(s): {key_pattern} due to redis connection."
            )
            return False

        try:
            cursor = 0
            total_deleted = 0
            while True:
                cursor, keys = self.client.scan(
                    cursor=cursor, match=key_pattern, count=100
                )
                if keys:
                    total_deleted += self.client.delete(*keys)
                if cursor == 0:
                    break

            if total_deleted > 0:
                self.logger.info(
                    f"Deleted {total_deleted} cache key(s) matching: {key_pattern}"
                )
                return True
            else:
                self.logger.info(f"No cache keys matched pattern: {key_pattern}")
                return False

        except redis.exceptions.TimeoutError:
            self.logger.error("Redis delete operation timed out.")
        except Exception as e:
            self.logger.error(
                f"Failed to delete cache key(s): {key_pattern} due to Error: {e}"
            )

        return False

    def get_size_info(self, key: str):
        """Retrieves size info of cache data.

        Args:
            key (str): Cache key.

        Returns:
            _type_: _description_
        """
        cache_result = None
        if not self.client:
            self.logger.info(
                f"Failed to debug cache key: {key} due to redis connection."
            )
            return cache_result

        try:
            cache_result = self.client.debug_object(key)
        except redis.exceptions.TimeoutError:
            self.logger.error("Redis debug object operation timed out.")
        except Exception as e:
            self.logger.error(
                f"Failed to get size by cache key: {key} due to error: {e}"
            )

        return cache_result

    def get_values_by_pattern(self, pattern: str):
        """Retrieves all cache values that match a given pattern.

        Args:
            pattern (str): The Redis key pattern, e.g., "supercard:*"

        Returns:
            dict: A dictionary mapping keys to their corresponding values.
        """
        result = {}
        if not self.client:
            self.logger.info(
                f"Failed to get cache pattern: {pattern} due to redis connection."
            )
            return result

        try:
            print("Cache Get Here")
            cursor = 0
            matched_keys = []
            # Use SCAN to safely iterate (non-blocking)
            while True:
                cursor, keys = self.client.scan(cursor=cursor, match=pattern, count=100)
                matched_keys.extend(keys)
                if cursor == 0:
                    break

            if matched_keys:
                # Fetch all values in one go
                values = self.client.mget(matched_keys)
                for key, raw_value in zip(matched_keys, values):
                    if raw_value is not None:
                        try:
                            import json

                            result[key] = json.loads(raw_value)
                        except (ValueError, TypeError):
                            result[key] = raw_value  # Keep as raw bytes if not JSON

        except redis.exceptions.TimeoutError:
            self.logger.error("Redis SCAN/MGET operation timed out.")
        except Exception as e:
            self.logger.error(
                f"Failed to get cache values for pattern {pattern} due to error: {e}"
            )

        return result


# Cerebro Redis
redis_cache_client = RedisCacheClient(db_settings.REDIS_URI, logger=app_logger)
redis_cache_client.open()

redis_client = None
if redis_cache_client.is_connected():
    redis_client = redis_cache_client.connection()


def get_cache_client():
    """Retrieves actived redis cache client."""
    return redis_cache_client
