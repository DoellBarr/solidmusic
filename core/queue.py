from typing import Dict, List


class Queue:
    def __init__(self):
        self.__queue: Dict[int, List[Dict[str, str]]] = {}

    def insert_one(self, chat_id: int, objects: Dict[str, str]):
        if chat_id not in self.__queue:
            self.__queue[chat_id] = [objects]
            queue = self.__queue[chat_id]
        else:
            queue = self.__queue[chat_id]
            queue.extend([objects])

    def delete_one(self, chat_id: int):
        if chat_id not in self.__queue:
            return "not_in_queue"
        self.__queue[chat_id].pop(0)

    def delete_chat(self, chat_id: int):
        if chat_id not in self.__queue:
            return "not_in_queue"
        del self.__queue[chat_id]

    def get(self, chat_id: int):
        return self.__queue[chat_id][0]

    @property
    def playlist(self):
        return self.__queue
