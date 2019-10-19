import json, time
import requests


PROXY_ADDR = 'http://127.0.0.1:8000/redisproxy'


def test_verify(test, expected, actual, msg):
    print('Test:', test)
    result = 'PASS' if expected == actual else 'FAIL'
    print('{} - Expected: {} Actual: {}'.format(result, expected, actual))
    if expected != actual:
        print(msg)
    print


print('Sleeping 5s to allow environment to be built...')
time.sleep(5)

## Tests

try:
    # 1. Invalid method
    res = requests.put(PROXY_ADDR + '/get/abc')
    test_verify('Invalid http method', 403, res.status_code, 'Status code should match')

    # 2. Invalid url
    res = requests.get(PROXY_ADDR + '/yeet/abc')
    test_verify('Invalid url', 404, res.status_code, 'Status code should match')

    # # 3. Missing key params
    res = requests.get(PROXY_ADDR + '/get/')
    test_verify('Missing params', 404, res.status_code, 'Status code should match')

    # # 4. Cache misses
    res = requests.get(PROXY_ADDR + '/get/nas')
    test_verify('Missing params', 404, res.status_code, 'Status code should match')
    test_verify('Item not found', 'No value for key: nas', res.text, 'Value should match')

    # # 5. Cache hit
    # # First place value in the cache
    res = requests.put(PROXY_ADDR + '/set/milesdavis', json={'val':'kind of blue'})

    res = requests.get(PROXY_ADDR + '/get/milesdavis')
    test_verify('Invalid status code', 200, res.status_code, 'Status code should match')
    test_verify('Item found', 'kind of blue', res.text, 'Value should match')
except Exception as e:
    print(f'Error running e2e tests {e}')