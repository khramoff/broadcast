import networkx as nx
import sys
import netw
import message
import matplotlib.pyplot as plt

g = nx.complete_graph(range(int(sys.argv[1])))
# g = nx.dense_gnm_random_graph(int(sys.argv[1]), int(sys.argv[2]))

plt.subplot(121)
nx.draw(g)
ntw = netw.Network(g)
#
mess = message.Message()
# ntw.add_message(mess, (0, 1))
ntw.add_msg_random(mess)
results = []

for i in range (1, 1000):
    ntw.broadcast(i)
    results.append(ntw.message_count)

plt.subplot(122)
plt.plot(results)
plt.show()
#