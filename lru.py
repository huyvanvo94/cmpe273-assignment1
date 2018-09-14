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

class LRU:
    def __init__(self, max):
        self.max = max
        self.lst = []

    def append(self, element):
        if len(self.lst) > self.max:
            del self.lst[0]

        self.lst.append(element)


class ChatHistory:
    def __init__(self, max):
        self.size = max
        self.chats = []

    def stream(self, request, context):
        lastindex = 0
        lastuuid = None

        while True:
            if 0 < len(self.chats) <= lastindex and lastuuid is not None and lastuuid != self.chats[0].uuid:
                yield self.chats[len(self.chats) - 1]
            else:
                while lastindex < len(self.chats):
                    n = self.chats[lastindex]

                    lastindex += 1
                    yield n

            if len(self.chats) > 0:
                lastuuid = self.chats[0].uuid

    def append(self, element):
        if len(self.chats) > self.size:
            del self.chats[0]

        self.chats.append(element)
