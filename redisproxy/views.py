from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from .cache import LruCache
from .redis import create_redis_client

import json, logging, os

cache = LruCache(int(os.getenv("CACHE_CAPACITY", 64)), int(os.getenv("CACHE_EXPIRY", 3600)))
logger = logging.getLogger("redisproxy.views")
redis_client = create_redis_client()


def index(request):
    return HttpResponse("Hello! This is the RedisProxy index. Make a request to /redisproxy/<your-key> to try the proxy cache!")


def get_val(request, key):
    """
    Attempts to get a matching value for a given key from the local cache, 
    if that fails requests the value from redis
    """
    logging.info(f'Received get request for key {key}')

    val = cache.get(key)
    if val == None:
        logging.info(f'Local cache miss - going to redis for key {key}')
        try:
            val = redis_client.get(key)
            if val == None:
                return HttpResponseNotFound(f'No value for key: {key}')
        except Exception as e:
            logging.error(f'Error getting value from redis: {e}')
            return HttpResponseNotFound(f'No value for key: {key}')

    return HttpResponse(val)


@csrf_exempt
def set_key(request, key):
    """
    This method exists purely for testing purposes to allows us to place items in redis' cache
    """
    if request.method != "PUT":
        logging.error(f' Received bad request for {request.path} - http method = {request.method}')
        return HttpResponseBadRequest("Invalid HTTP request method")

    body = json.loads(request.body)
    if "val" not in body:
        logging.error(f' Received bad request - missing set value in body {body}')
        return HttpResponseBadRequest("Missing 'val' in request body")

    logging.info(f'Received set request for pair {key}:{body["val"]}')
    
    # For the purpose of this demo I only want to place it into redis
    # So the proxy's get functionality can be tested against it
    try:
        redis_client.set(key, body["val"])
    except Exception as e:
        logging.error(f'Error setting value in redis cache {e}')
        return HttpResponseBadRequest(f'Unable to set {key} to {body["val"]} in Redis.')

    return HttpResponse(f'Set {key} to val {body["val"]}')