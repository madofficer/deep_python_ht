# from collections.abc import Hashable
# from typing import Any
#
#
# class DLLNode:
#     def __init__(self, key: Hashable, val: Any):
#         self.key, self.val = key, val
#         self.prev = self.next = None
#
#
# class LRUCache:
#     def __init__(self, capacity=None):
#         self._capacity = 2 if capacity is None else capacity
#         self._cache = {}
#         self._left, self._right = DLLNode(0, 0), DLLNode(0, 0)
#         self._left.next, self._right.prev = self._right, self._left
#
#     def _remove(self, node: DLLNode) -> None:
#         prev, nxt = node.prev, node.next
#         prev.next, nxt.prev = nxt, prev
#
#     def _insert(self, node: DLLNode) -> None:
#         prev, nxt = self._right.prev, self._right
#         prev.next = nxt.prev = node
#         node.next, node.prev = nxt, prev
#
#     def get(self, key: Hashable) -> Any:
#         if key in self._cache:
#             self._remove(self._cache[key])
#             self._insert(self._cache[key])
#             return self._cache[key].val
#         return None
#
#     def set(self, key: Hashable, val: Any) -> None:
#         if key in self._cache:
#             self._remove(self._cache[key])
#         self._cache[key] = DLLNode(key, val)
#         self._insert(self._cache[key])
#
#         if len(self._cache) > self._capacity:
#
#             lru = self._left.next
#             self._remove(lru)
#             del self._cache[lru.key]
