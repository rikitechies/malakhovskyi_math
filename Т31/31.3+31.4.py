import threading
import time
import random
import string
from collections import deque

class Message:
    def __init__(self, msg_id, is_priority=False):
        self.id = msg_id
        self.is_priority = is_priority
        self.data = self._generate_payload(16)

    def _generate_payload(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    def __str__(self):
        status = "[!]" if self.is_priority else "[.]"
        return f"{status} Повідомлення №{self.id}"
import threading
import time
import random
import string
from collections import deque

class Message:
    def __init__(self, msg_id, is_priority=False):
        self.id = msg_id
        self.is_priority = is_priority
        self.data = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    def __str__(self):
        status = "[!]" if self.is_priority else "[.]"
        return f"{status} Повідомлення №{self.id}"

class PriorityQueue(deque):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()

    def put(self, message):
        with self._lock:
            if not message.is_priority:
                self.append(message)
            else:
                idx = 0
                for item in self:
                    if item.is_priority:
                        idx += 1
                    else:
                        break
                self.insert(idx, message)

    def get(self):
        with self._lock:
            return self.popleft() if self else None

T1 = 2
T2 = 6

def producer(q):
    count = 1
    while True:
        time.sleep(random.uniform(1, T1))
        is_prio = random.random() < 0.45
        new_msg = Message(count, is_priority=is_prio)
        q.put(new_msg)
        print(f"ГЕНЕРАТОР: Додано {new_msg}")
        count += 1

def consumer(q):
    while True:
        msg = q.get()
        if msg:
            print(f"ОБРОБНИК: Робота з №{msg.id}")
            time.sleep(random.uniform(1, T2))
            print(f"ОБРОБНИК: Результат №{msg.id}: {msg.data}")
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    msg_queue = PriorityQueue()

    print("Програма запущена. Натисніть ENTER для завершення роботи.")
    print("-" * 40)

    t1 = threading.Thread(target=producer, args=(msg_queue,), daemon=True)
    t2 = threading.Thread(target=consumer, args=(msg_queue,), daemon=True)

    t1.start()
    t2.start()

    input()
    
    print("Роботу програми завершено.")