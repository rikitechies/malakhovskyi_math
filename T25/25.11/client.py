import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    welcome = client.recv(1024).decode('utf-16')
    print(welcome)

    am_i_first = "Клієнт 1" in welcome

    while True:
        if am_i_first:
            msg = input("Ви: ")
            client.send(msg.encode('utf-16'))
            if msg.lower() == 'exit': break
            
            print("Чекаємо відповідь...")
            data = client.recv(1024).decode('utf-16')
            print(f"Співрозмовник: {data}")
        else:
            print("Чекаємо повідомлення...")
            data = client.recv(1024).decode('utf-16')
            print(f"Співрозмовник: {data}")
            
            msg = input("Ви: ")
            client.send(msg.encode('utf-16'))
            if msg.lower() == 'exit': break

    client.close()

if __name__ == "__main__":
    start_client()