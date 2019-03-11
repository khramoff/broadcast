class Message:
    def __init__(self, with_ttl):
        self.__with_ttl = with_ttl
        self.__ttl = -1

    @property
    def ttl(self):
        return self.__ttl

    @ttl.setter
    def ttl(self, ttl):
        self.__ttl = ttl

    @property
    def with_ttl(self):
        return self.__with_ttl

    @with_ttl.setter
    def with_ttl(self, with_ttl):
        self.__with_ttl = with_ttl

    def inc_ttl(self):
        self.__ttl += 1

    def dec_ttl(self):
        self.__ttl -= 1

