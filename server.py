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
max_call_per_30_seconds_per_user = doc['max_call_per_30_seconds_per_user']
# the users online

usersOnline = {}

limit = 10  # 30


def rate(func):
    def called(self, request):
        global usersOnline
        user = request.uuid

        # first
        if user not in usersOnline:
            timestamp = 0
            count = 1
            usersOnline[user] = (timestamp, count)
            print(1)

            func(self, request)
            return

        global max_num_messages_per_user

        timestamp = usersOnline[user][0]
        count = usersOnline[user][1]

        diff = time.time() - timestamp

        if (count >= max_call_per_30_seconds_per_user and diff < limit) != False or count == 0 and diff < limit:
            print('YO')

            return

        if count < max_call_per_30_seconds_per_user and diff >= limit:
            print(3)
            count += 1

            func(self, request)
            if count >= max_call_per_30_seconds_per_user:
                count = 0
                timestamp = time.time()

            usersOnline[user] = (timestamp, count)

    return called


def lru_cache(func):
    def cache(self, request):
        print(' i am called ')

        if request.chatChannel not in self.chatChannels:
            self.chatChannels[request.chatChannel] = Channel(capacity=max_num_messages_per_user)

        if request.chatChannel in self.chatChannels:
            self.chatChannels[request.chatChannel].append(request)

        return func(self, request)

    return cache


class ChatService(message_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chatChannels = {}
        self.max = 1
        self.index = 0
        self.lastKnown = 0
        self.cache = LRUCache(capacity=self.max)
        self.lastMessage = None
        self.channels = []
        self.recent = {}

    def ReceiveMsg(self, request, context):
        allmsg = False
        lastindex = 0

        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:

            try:
                channel = self.chatChannels[request.chatChannel]
                # Check if there are any new messages


                while channel.index > lastindex and allmsg == False:
                    print('cache')
                    n = channel.get(lastindex)
                    lastindex += 1
                    if n != -1:
                        yield n
                    else:
                        channel.lastKnown = n

                if allmsg == False:
                    print('yo!!!')
                    self.recent[request.chatChannel] = None
                    allmsg = True
                    continue

                if allmsg:

                    if not self.recent[request.chatChannel] is None:
                        print('recent')
                        yield self.recent[request.chatChannel]

                        self.recent[request.chatChannel] = None


            except:
                pass
            #  print("error")

    # @lru_cache

    def SendNote(self, request, context):

        response = message_pb2.Empty()
        response.chatChannel = request.chatChannel

        self.handleRequest(request)

        return response

    @rate
    def handleRequest(self, request):
        self.save(request)


    @lru_cache
    def save(self, request):
        name = request.chatChannel
        self.recent[name] = request


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



# Limit how many time users can send to server
class UsersManager:
    def __init__(self):
        self.users = {}
        # TODO: Change this when turning in
        self.limit = 10  # 30 seconds

    def isOnline(self, uuid):
        return uuid in self.users

    def msgReceived(self, uuid):
        if uuid not in self.users:
            self.users[uuid] = (0, 0)


manager = UsersManager()
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
