#!/usr/bin/env python3
""" Module: Redis Server,  Implementing an
expiring web cache and tracker"""
import redis
import requests

redis_client = redis.Redis()

def get_page(url: str) -> str:
    """Function: expiring web cache and tracker"""

    cached = redis_client.get(f"cached:{url}")
    if cached is not None:
        redis_client.incr(f"count:{url}")
        redis_client.expire(f"count:{url}", 10)
        return cached.decode('utf-8')

    response = requests.get(url)
    redis_client.set(f"cached:{url}", response.text)
    redis_client.incr(f"count:{url}")
    redis_client.expire(f"cached:{url}", 10)
    redis_client.expire(f"count:{url}", 10)

    return response.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')