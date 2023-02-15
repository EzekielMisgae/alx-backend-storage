#!/usr/bin/env python3
""" Module: Redis Server,  Implementing an
expiring web cache and tracker"""
import redis
import requests

redis = redis.Redis()
incr = 0

def get_page(url: str) -> str:
    """Function: expiring web cache and tracker"""

    response = requests.get(url)
    redis.set(f"cached:{url}", incr)
    redis.incr(f"count:{url}")
    redis.setex(f"cached:{url}", 10, redis.get(f"cached:{url}"))
    return response.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')