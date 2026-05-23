import random
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


cache = LRUCache(1000)


def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right):
    key = (left, right)

    cached_result = cache.get(key)

    if cached_result != -1:
        return cached_result

    result = sum(array[left:right + 1])
    cache.put(key, result)

    return result


def update_with_cache(array, index, value):
    array[index] = value

    keys_to_delete = []

    for left, right in cache.cache.keys():
        if left <= index <= right:
            keys_to_delete.append((left, right))

    for key in keys_to_delete:
        del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]

    queries = []

    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)

            queries.append(("Range", left, right))

    return queries


def run_without_cache(array, queries):
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_no_cache(array, left, right)
        elif query[0] == "Update":
            _, index, value = query
            update_no_cache(array, index, value)


def run_with_cache(array, queries):
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_with_cache(array, left, right)
        elif query[0] == "Update":
            _, index, value = query
            update_with_cache(array, index, value)


def main():
    random.seed(42)

    n = 100_000
    q = 50_000

    original_array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    array_no_cache = original_array.copy()
    array_with_cache = original_array.copy()

    start = time.perf_counter()
    run_without_cache(array_no_cache, queries)
    time_no_cache = time.perf_counter() - start

    start = time.perf_counter()
    run_with_cache(array_with_cache, queries)
    time_with_cache = time.perf_counter() - start

    speedup = time_no_cache / time_with_cache

    print(f"Без кешу : {time_no_cache:.2f} c")
    print(f"LRU-кеш  : {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")


if __name__ == "__main__":
    main()