"""Minimal wire-compatible messages from Google's published stream_list.proto.

Source: https://developers.google.com/youtube/data/live/streaming-live-chat
Unknown fields are intentionally ignored by protobuf.
"""


def messages():
    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

    file = descriptor_pb2.FileDescriptorProto(name="stream_studio_chat.proto", package="youtube.api.v3", syntax="proto2")
    string = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
    message_type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
    optional = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
    repeated = descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED

    def make(name, fields):
        message = file.message_type.add(name=name)
        for field_name, number, kind, label, type_name in fields:
            field = message.field.add(name=field_name, number=number, type=kind, label=label)
            if type_name:
                field.type_name = ".youtube.api.v3." + type_name

    make("Request", [("live_chat_id", 1, string, optional, None),
                     ("page_token", 99, string, optional, None),
                     ("part", 100, string, repeated, None)])
    make("Snippet", [("published_at", 4, string, optional, None),
                     ("display_message", 16, string, optional, None)])
    make("Author", [("display_name", 103, string, optional, None)])
    make("Message", [("id", 101, string, optional, None),
                     ("snippet", 2, message_type, optional, "Snippet"),
                     ("author_details", 3, message_type, optional, "Author")])
    make("Response", [("offline_at", 2, string, optional, None),
                      ("next_page_token", 100602, string, optional, None),
                      ("items", 1007, message_type, repeated, "Message")])
    pool = descriptor_pool.DescriptorPool()
    pool.Add(file)
    return tuple(message_factory.GetMessageClass(pool.FindMessageTypeByName("youtube.api.v3." + name))
                 for name in ("Request", "Response"))
