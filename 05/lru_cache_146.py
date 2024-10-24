from collections.abc import Hashable

from typing_extensions import Optional


class DLLNode:
    def __init__(self, key: Hashable, val: Optional[any]):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.left, self.right = DLLNode(0, 0), DLLNode(0, 0)
        self.left.next, self.right.prev = self.right, self.left

    def _remove(self, node: DLLNode) -> None:
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node: DLLNode) -> None:
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.next, node.prev = nxt, prev

    def get(self, key: Hashable):
        if key in self.cache:
            self._remove(self.cache[key])
            self._insert(self.cache[key])
            return self.cache[key].val
        return -1

    def set(self, key: Hashable, val: any) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        self.cache[key] = DLLNode(key, val)
        self._insert(self.cache[key])

        if len(self.cache) > self.capacity:

            lru = self.left.next
            self._remove(lru)
            del self.cache[lru.key]


if __name__ == "__main__":
    obj = LRUCache(2)
    param_1 = obj.get(1)
    print(param_1)
    obj.set(1, 1)
    print(obj.get(1))
    obj.set('1', 'str')
    obj.set((1, 2), 'val2')
    print(obj.get(1))
    print(obj.get('1'))
    print(obj.get((1, 2)))
