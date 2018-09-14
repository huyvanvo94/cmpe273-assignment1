# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import message_pb2 as message__pb2


class ChatServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ChatStream = channel.unary_stream(
        '/ChatServer/ChatStream',
        request_serializer=message__pb2.Empty.SerializeToString,
        response_deserializer=message__pb2.Note.FromString,
        )
    self.SendNote = channel.unary_unary(
        '/ChatServer/SendNote',
        request_serializer=message__pb2.Note.SerializeToString,
        response_deserializer=message__pb2.Empty.FromString,
        )


class ChatServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ChatStream(self, request, context):
    """This bi-directional stream makes it possible to send and receive Notes between 2 persons
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendNote(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ChatStream': grpc.unary_stream_rpc_method_handler(
          servicer.ChatStream,
          request_deserializer=message__pb2.Empty.FromString,
          response_serializer=message__pb2.Note.SerializeToString,
      ),
      'SendNote': grpc.unary_unary_rpc_method_handler(
          servicer.SendNote,
          request_deserializer=message__pb2.Note.FromString,
          response_serializer=message__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ChatServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
