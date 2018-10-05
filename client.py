#TODO: update implementation limit on server side


import sys
import threading
import grpc
import time
import uuid
# import the generated classes
import message_pb2 as chat
import message_pb2_grpc as rpc
from security import AESCipher
from tkinter import *

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
print(doc)

# open a gRPC channel

count = 0

KEY = "hello world"

cipher = AESCipher(key=KEY)


def rate(func):
    # TODO: Change this when turning in
    limit = 10 # 30 seconds

    def called(*args, **kwargs):
        global max_call_per_30_seconds_per_user, count

        diff = time.time() - called.timestamp
        print(diff)
        print('count ', count)
        print(count >= max_call_per_30_seconds_per_user and diff < limit)
        if (count >= max_call_per_30_seconds_per_user and diff < limit) != False:
            print('YO')
            return

        if count == 0 and diff < limit:
            return

        if count < max_call_per_30_seconds_per_user and diff >= limit:

            print('a')
            count += 1
            func(*args, **kwargs)
            if count >= max_call_per_30_seconds_per_user:
                count = 0
                called.timestamp = time.time()

        print('yo')

    called.timestamp = 0

    return called


def encrypt(n):
    return cipher.encrypt(n)


def decrypt(n):
    return cipher.decrypt(n)


class Client:

    def __init__(self, u: str, window, chatName):
        # the frame to put ui components on
        self.window = window
        self.username = u
        self.last = 0
        # create a gRPC channel + stub
        channel = grpc.insecure_channel('localhost:50051')
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages

        """
        print(' listen for messages ')
        request = chat.Empty()
        request.chatChannel = chatName


        for note in self.conn.ChatStream(request):
            print(' i am called ')
            if not note is None:
                print('foo bza')
                name = decrypt(note.name)
                message = decrypt(note.message)
                self.chat_list.insert(END, "[{}] {}\n".format(name, message))

    @staticmethod
    def send_message(entry_message, message, name, uuid, conn, chatChannel):
        entry_message.delete(0, 'end')
        n = chat.Note()
        n.name = encrypt(name)
        n.message = encrypt(message)
        n.uuid = str(uuid)

        n.chatChannel = chatChannel
        conn.SendNote(n)

    def send_action(self, event):

        """
        This method is called when user enters something into the textbox
        """
        message = self.entry_message.get()

        if message is not '':
            self.send_message(self.entry_message, message, self.username, self.username, self.conn, chatName)


    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_action)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    username = sys.argv[1]

    print('[Spartan] Connected to Spartan Server at port {}.'.format(port))
    print('[Spartan] User list: {}'.format(users))

    for group in groups:

        print('[Spartan] Group list: {}'.format(group))
    chatName = 'group1'
    channelName = input('[Spartan] Enter a user/group whom you want to chat with:')
    # user did not put in chat name
    if channelName == '':
        channelName = username.lower()

    else:
        print('[Spartan] You are now ready to chat with {}.'.format(channelName))
        channelName = channelName.lower()

    chatName = channelName

    if chatName is None:
        chatName = input("channel name: ")

    print(channelName)

    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()

    root.deiconify()
    c = Client(username, frame, chatName)
