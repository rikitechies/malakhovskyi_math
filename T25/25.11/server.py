import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(2)
    print("Сервер запущено. Очікування двох клієнтів...")

    conn1, addr1 = server.accept()
    print(f"Клієнт 1 підключився: {addr1}")
    conn1.send("Ви Клієнт 1. Очікуйте...".encode('utf-16'))

    conn2, addr2 = server.accept()
    print(f"Клієнт 2 підключився: {addr2}")
    conn2.send("Ви Клієнт 2. Починаємо чат!".encode('utf-16'))

    while True:
        msg1 = conn1.recv(1024)
        if not msg1 or msg1.decode('utf-16').lower() == 'exit': break
        print(f"Клієнт 1 каже: {msg1.decode('utf-16')}")
        conn2.send(msg1)

        # 2. Читаємо від Клієнта 2 -> Передаємо Клієнту 1
        msg2 = conn2.recv(1024)
        if not msg2 or msg2.decode('utf-16').lower() == 'exit': break
        print(f"Клієнт 2 каже: {msg2.decode('utf-16')}")
        conn1.send(msg2)

    print("Чат завершено.")
    conn1.close()
    conn2.close()
    server.close()

if __name__ == "__main__":
    start_server()