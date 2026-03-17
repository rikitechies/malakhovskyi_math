import socket

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5000))
    sock.listen(1)
    print("Сервер очікує файл...")

    conn, addr = sock.accept()

    with open('received_data.txt', 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print("Файл отримано та збережено як 'received_data.txt'")
    conn.close()
    sock.close()

if __name__ == "__main__":
    start_server()