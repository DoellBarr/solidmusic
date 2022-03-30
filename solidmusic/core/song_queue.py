class Queue:
    def __init__(self):
        self.__queue: dict[int, list[dict[str, str]]] = {}

    async def insert_one(self, chat_id: int, datas: dict[str, str]):
        if chat_id not in self.__queue:
            self.__queue[chat_id] = [datas]
        else:
            self.__queue[chat_id].extend([datas])
        return self.__queue[chat_id]

    async def delete_one(self, chat_id: int):
        return None if chat_id not in self.__queue else self.__queue[chat_id].pop(0)

    async def delete_chat(self, chat_id: int):
        if chat_id not in self.__queue:
            return None
        del self.__queue[chat_id]

    async def get_queue(self, chat_id: int):
        return self.__queue[chat_id][0]

    @property
    def playlist(self):
        return self.__queue


queue = Queue()
