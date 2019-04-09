class Message:
    def __init__(self):
        self.__time = 0
        self.id = 0
        self.sender = -1
        self.receiver = -1

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
