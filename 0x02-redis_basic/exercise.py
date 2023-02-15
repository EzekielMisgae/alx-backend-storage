#!/usr/bin/env python3
"""
Redis module, Writing strings to Redis
Reading from Redis and recovering original type
Incrementing values, storing lists, Retrieving lists
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools
from functools import wraps

class Cache():
    """
    Store instance of Redis client as private variable _redis
    Flush the instance using flushdb
    """
    def __init__(self):
        """
        Prototype: def __init__(self):
        Store instance of Redis client as private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = lambda x: x) -> Union[bytes, str, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, lambda x: x.decode())

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, lambda x: int(x.decode()))

    def count_calls(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapped(self, *args, **kwargs):
            key = fn.__qualname__
            self._redis.incr(key)
            return fn(self, *args, **kwargs)
        return wrapped

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key