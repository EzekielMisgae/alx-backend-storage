#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests
from functools import wraps
from typing import Callable

redis = redis.Redis()

def cache_expiring(ttl: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            url = args[0]
            cached_content = redis.get(f"cached:{url}")
            if cached_content is not None:
                return cached_content.decode("utf-8")
            else:
                resp = requests.get(url)
                redis.incr(f"count:{url}")
                redis.set(f"cached:{url}", resp.content)
                redis.expire(f"cached:{url}", ttl)
                return resp.text
        return wrapper
    return decorator

@cache_expiring(10)
def get_page(url: str) -> str:
    """Function: expiring web cache and tracker"""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk') 