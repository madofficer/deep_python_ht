import logging
import argparse
from collections.abc import Hashable
from typing import Any
from functools import wraps



def setup_logging(log_to_stdout=False, custom_filter=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('cache.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_to_stdout:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.INFO)
        stdout_formatter = logging.Formatter('%(levelname)s - %(message)s')
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)

    if custom_filter is not None:
        logger.addFilter(custom_filter)


def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logging.info(f'Function: {func.__name__} returned: {result}')
        return result

    return wrapper


class DLLNode:
    def __init__(self, key: Hashable, val: Any):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int = 2):
        self._capacity = capacity
        self._cache = {}
        self._left, self._right = DLLNode(0, 0), DLLNode(0, 0)
        self._left.next, self._right.prev = self._right, self._left

    def _remove(self, node: DLLNode) -> None:
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev
        logging.debug(f'Removed node with key: {node.key}')

    def _insert(self, node: DLLNode) -> None:
        prev, nxt = self._right.prev, self._right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev
        logging.debug(f'Inserted node with key: {node.key}')

    @log_function_call
    def get(self, key: Hashable) -> Any:
        if key in self._cache:
            self._remove(self._cache[key])
            self._insert(self._cache[key])
            return self._cache[key].val

        logging.warning(f'Key not found: {key}')
        return None

    @log_function_call
    def set(self, key: Hashable, val: Any) -> None:
        if key in self._cache:
            self._remove(self._cache[key])

        logging.info(f'Setting new key: {key} with value: {val}')
        self._cache[key] = DLLNode(key, val)
        self._insert(self._cache[key])

        if len(self._cache) > self._capacity:
            lru = self._left.next
            logging.info(f'Removing least recently used key: {lru.key}')
            self._remove(lru)
            del self._cache[lru.key]


class WordCountFilter(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2 != 0


def main():
    parser = argparse.ArgumentParser(description='LRU Cache with Logging')
    parser.add_argument('-s', action='store_true', help='Log to stdout')
    parser.add_argument('-f', action='store_true', help='Apply custom filter')

    args = parser.parse_args()

    custom_filter = WordCountFilter() if args.f else None
    setup_logging(log_to_stdout=args.s, custom_filter=custom_filter)

    # Пример операций с кэшем
    cache = LRUCache(capacity=3)

    cache.set('a', 1)
    cache.set('b', 2)

    print(cache.get('a'))
    print(cache.get('c'))

    cache.set('c', 3)
    cache.set('d', 4)

    print(cache.get('b'))


if __name__ == "__main__":
    main()