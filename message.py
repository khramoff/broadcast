class Message:
    def __init__(self, id, destination):
        self.__time = 0
        self.id = id
        self.stamp = 0
        self.sender = -1
        self.receiver = -1
        self.destination = -1

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    def inc_time(self):
        self.__time += 1

    def dec_time(self):
        self.__time -= 1
