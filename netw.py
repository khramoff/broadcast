import networkx as nx
from functools import partial
from operator import is_not

class Network:

    def __init__(self, g):
        self.__graph = g
        self.__message_count = 0

    @property
    def graph(self):
        return self.__graph

    @property
    def message_count(self):
        return self.__message_count

    @graph.setter
    def graph(self, g):
        self.__graph = g

    @message_count.setter
    def message_count(self, count):
        self.__message_count = count

    def inc_message_count(self):
        self.__message_count += 1

    def dec_message_count(self):
        self.__message_count -= 1

    def add_msg_random(self, msg):
        for edge in nx.edges(self.graph):
            self.add_message(msg, edge)
            break
    def add_message(self, message, edge):
        message.sender = edge[0]
        message.receiver = edge[1]
        self.inc_message_count()
        message.id = self.message_count
        msg = nx.get_edge_attributes(self.graph, 'messages')
        new_messages = list()
        if edge in msg.keys():
            old_messages = msg[edge]
            new_messages.extend(map((lambda x: x.inc_time()), filter(partial(is_not, None), old_messages)))
        new_messages.append(message)
        self.graph[edge[0]][edge[1]]['messages'] = new_messages

    def broadcast(self, time):
        msg = nx.get_edge_attributes(self.graph, 'messages')
        for edge in nx.edges(self.graph):
            if edge not in msg.keys():
                continue

            messages = list(filter(partial(is_not, None), msg[edge]))
            for message in messages:
                m = [i for i in messages if i.id != message.id]
                self.dec_message_count()
                self.graph[edge[0]][edge[1]]['messages'] = m
                message.inc_time()
                sender = message.sender
                message.sender = message.receiver
                for neighbour in nx.all_neighbors(self.graph, message.receiver):
                    if neighbour == sender:
                        continue
                    message.receiver = neighbour
                    self.add_message(message, (message.sender, message.receiver))

