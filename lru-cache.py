
"""
lru-cache.py
@author: huy vo 
lru cache implementation
"""

from collections import deque


class LRUCache(object):

    def __init__(self, capacity):
        self.size = capacity

        self.q = deque()
        self.pages = {}

    def put(self, key, value):

        if key not in self.pages:

            if len(self.q) >= self.size:
                key2 = self.q.popleft()
                del self.pages[key2]
            self.q.append(key)
            self.pages[key] = value
        else:
            self.pages[key] = value
            self._moveFrontOfQueue(key)

    def get(self, key):
        if key in self.pages:
            self._moveFrontOfQueue(key)
            return self.pages[key]

        return -1

    def _moveFrontOfQueue(self, key):
        self.q.remove(key)
        self.q.append(key)
