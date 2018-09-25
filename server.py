import grpc
from concurrent import futures
from lru import LRUCache

import time
import message_pb2
import message_pb2_grpc


def lru_cache(state, func):
    def cache(*args, **kwargs):
        if state == 'cache':
            cache.messages.put(*args, **kwargs)

            pass

        if state == 'fetch':
            pass

    cache.messages = LRUCache(capacity=20)


class ChatService(message_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chatChannels = {}
        self.max = 1
        self.index = 0
        self.lastKnown = 0
        self.cache = LRUCache(capacity=self.max)

    def ChatStream(self, request, context):

        lastindex = 0

        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:

            try:
                channel = self.chatChannels[request.chatChannel]
                # Check if there are any new messages
                while channel.index > lastindex:
                    n = channel.get(lastindex)
                    print(n)
                    lastindex += 1
                    if n != -1:
                        yield n
                    else:
                        channel.lastKnown = n
            except:
                pass
              #  print("error")

    def SendNote(self, request, context):

        if request.chatChannel not in self.chatChannels:
            self.chatChannels[request.chatChannel] = Channel(10)

        try:
            self.chatChannels[request.chatChannel].append( request )
        except:
            print("not in chat")
        #  self.cache.put(self.index, request)
        # self.index += 1
        ''' 
        if len(self.chats) >= self.max:
            del self.chats[0]

        self.chats.append(request)'''

        response = message_pb2.Empty()
        response.chatChannel = request.chatChannel

        return response


class Channel(object):
    def __init__(self, capacity):
        self.cache = LRUCache(capacity=capacity)
        self.index = 0
        self.lastKnow = 0

    def append(self, note):
        self.cache.put(self.index, note)
        self.index += 1

    def get(self, page):
        return self.cache.get(page)


def send(server, request): pass


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

message_pb2_grpc.add_ChatServerServicer_to_server(ChatService(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
