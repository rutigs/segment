## README

### Instructions

First, git clone the project somewhere on your computer.
The proxy and its backing Redis instance can be ran via:

```
make run
```

The test suite; including unit and end to end testing can be ran via:

```
make test
```

### High Level Architecture

This `Redis` Proxy is written in `Python` using the `Django` Web Framework. The LRU cache is implemented in pure `Python` and takes advantage of the `OrderedDict` data structure in the standard library.

The application and `Redis` instances are ran inside of their own `Docker` containers, orchestrated by `Docker-Compose`.
The test suite runs the full fledged system as well as an additional container running black box end-to-end tests.

### What The Code Does

Configurable elements are laid out via Docker-Compose which then starts the Redis container and then the application container.
Django then handles most of the server setup and registers its urls to their corresponding views that I've written.

The `Get` endpoint first checks if a value is in the local cache and if not, makes a request to Redis to see if it has it.

The cache takes advantage of the `OrderedDict` in the python standard library to make the LRU requirements trivial. This allows it to simply pop the oldest item when the cache needs to. On cache hits, first it will pop the value, then it will check if it has expired using its expiry map, and if it hasn't it will re-insert the item back into the cache to reset its position, and return the value.

### Cache Operation Complexity

- Get:

O(1) time on cache item retrieval as well as updating its LRU property

- Set:

Average = O(1) time on cache insertion on a non-full cache

Worst Case = O(n) time on cache insertion if the item is not in the cache already and if the cache is full to decide the oldest item to delete

### Time Split

- Planning = ~20 minutes
- LRU Cache + Tests = ~20 minutes
- HTTP Server = ~30 minutes
- Redis and Server Docker/Compose Setup = ~1 hour
- E2E Tests and Documentation = ~1 hour

### Requirements Not Met

I did not attempt the 2nd bonus requirement of having the proxy implement the Redis protocol. It should also be noted that I didn't attempt the 1st bonus requirement of parallel concurrent processing innately, but my solution should satisfy it by having a lock on the Lru cache operations.