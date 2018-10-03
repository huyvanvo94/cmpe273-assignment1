import grpc
from concurrent import futures
from lru import LRUCache

import time
import message_pb2
import message_pb2_grpc
import yaml
f = open('config.yaml', 'r')
doc = yaml.load(f)

users = doc['users']
port = doc['port']
max_num_messages_per_user = doc['max_num_messages_per_user']
groups = doc['groups']
group1 = groups['group1']
group2 = groups['group2']

def lru_cache(func):
    def cache(self, request, context):
        print(' i am called ')

        if request.chatChannel not in self.chatChannels:
            self.chatChannels[request.chatChannel] = Channel(capacity=max_num_messages_per_user)

        if request.chatChannel in self.chatChannels:
            self.chatChannels[request.chatChannel].append(request)

        return func(self, request, context)

    return cache


class ChatService(message_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chatChannels = {}
        self.max = 1
        self.index = 0
        self.lastKnown = 0
        self.cache = LRUCache(capacity=self.max)

        self.channels = []

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

    @lru_cache
    def SendNote(self, request, context):

        response = message_pb2.Empty()
        response.chatChannel = request.chatChannel

        return response

    def PushMsg(self, request, context):
        channel = request.channel
        content = request.content
        who = request.who 


        return message_pb2.Empty()

class Channel(object):
    def __init__(self, capacity):
        self.cache = LRUCache(capacity=capacity)
        self.index = 0
        self.lastKnow = 0

    def foo(self):
        pass

    def append(self, note):
        self.cache.put(self.index, note)
        self.index += 1

    def get(self, page):
        return self.cache.get(page)


def send(server, request): pass


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

message_pb2_grpc.add_ChatServerServicer_to_server(ChatService(), server)

print('Spartan server started on port {}.'.format(port))
server.add_insecure_port('[::]:50051')

server.add_insecure_port('[::]:{}'.format(port))
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
