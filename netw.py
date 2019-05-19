import networkx as nx
from functools import partial
from operator import is_not

class Network:

    def __init__(self, g):
        self.__graph = g
        self.__message_count = 0
        self.memory = False
        self.mem_threshold = 0
        nx.set_node_attributes(self.__graph, frozenset(), 'seen')

    def do_memorize(self):
        self.memory = True

    def undo_memorize(self):
        self.memory = False

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
        message.stamp = self.message_count
        msg = nx.get_edge_attributes(self.graph, 'messages')
        new_messages = list()
        if edge in msg.keys():
            old_messages = msg[edge]
            new_messages.extend(map((lambda x: x.inc_time()), filter(partial(is_not, None), old_messages)))
        new_messages.append(message)
        self.graph[edge[0]][edge[1]]['messages'] = new_messages

    def memorize(self, n, id):
        if not self.memory:
            return

        seen = list(self.graph.nodes[n]['seen'])
        seen.append(id)
        newSet = frozenset(seen)
        self.graph.nodes[n]['seen'] = newSet

    def broadcast(self, time):
        msg = nx.get_edge_attributes(self.graph, 'messages')
        for edge in nx.edges(self.graph):
            if edge not in msg.keys():
                continue

            messages = list(filter(partial(is_not, None), msg[edge]))
            for message in messages:
                m = [i for i in messages if i.stamp != message.stamp]
                self.dec_message_count()
                self.graph[edge[0]][edge[1]]['messages'] = m
                if message.receiver == message.destination:
                    print('Message ', message.id, 'delivered to ', message.destination)
                    continue

                message.inc_time()
                sender = message.sender
                message.sender = message.receiver
                for neighbour in nx.all_neighbors(self.graph, message.receiver):
                    if neighbour == sender:
                        continue
                    seen = self.graph.node[neighbour]['seen']
                    if message.id in seen:
                        continue
                    self.memorize(neighbour, message.id)
                    message.receiver = neighbour
                    self.add_message(message, (message.sender, message.receiver))

