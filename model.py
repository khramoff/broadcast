import networkx as nx
import netw
import sys
import message
import matplotlib.pyplot as plt
from random import choice
import getopt


def send(ntw, steps, messages):
    results = [1]
    for m in messages:
        ntw.add_msg_random(m)

    for i in range(1, steps):
        ntw.broadcast(i)
        results.append(ntw.message_count)
    return results


def run(file, memory, message_count, steps):
    g = nx.read_adjlist(file)

    plt.subplot(121)
    nx.draw(g)
    ntw = netw.Network(g)

    if memory:
        ntw.do_memorize()

    messages = [message.Message(id=i, destination=choice(list(g.nodes()))) for i in range(1, message_count + 1)]

    results = send(ntw, steps, messages)

    plt.subplot(122)
    plt.xlabel('message count')
    plt.ylabel('steps')
    plt.plot(results)
    plt.show()


def main(argv):
    adjlist = ''
    memory = False
    steps = 10
    message_count = 10
    try:
        opts, args = getopt.getopt(argv, "hma:s:c:", ["message_count=", "adjlist=", "memory=", "steps="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('model.py -a <adjlist_file> -m -a -s <number_of_steps>')
            sys.exit()
        elif opt in ("-a", "--adjlist"):
            adjlist = arg
        elif opt in ("-m", "--memory"):
            memory = True
        elif opt in ("-s", "--steps"):
            steps = int(arg)
        elif opt in ("-c", "--message_count"):
            message_count = int(arg)
        else:
            print('model.py -a <adjlist_file> -m -a -s <number_of_steps>')
            sys.exit()
    print("Graph adjlist file: "+adjlist)
    print("Number of steps: "+str(steps))
    print("Message count: "+str(message_count))
    print("Memorize messages:"+str(memory))
    run(adjlist, memory, message_count, steps)


if __name__ == "__main__":
    main(sys.argv[1:])
