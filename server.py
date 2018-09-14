import grpc
from concurrent import futures
from lru import LRUCache
from lru import ChatHistory


import time
import message_pb2
import message_pb2_grpc

class ChatService(message_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chats = []
        self.max = 1


    def ChatStream(self, request, context):

        lastindex = 0
        lastuuid = None

        while True:
            if 0 < len(self.chats) <= lastindex and lastuuid is not None and lastuuid != self.chats[0].uuid:
                lastuuid = self.chats[0].uuid
                yield self.chats[len(self.chats) - 1]
            else:
                while lastindex < len(self.chats):
                    n = self.chats[lastindex]
                    lastuuid = self.chats[0].uuid
                    lastindex += 1
                    yield n





    def SendNote(self, request, context):

        if len(self.chats) >= self.max:
            del self.chats[0]

        self.chats.append(request)

        return message_pb2.Empty()




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