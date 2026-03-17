import socket

def send_file():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5000))

    filename = 'test.txt'
    
    try:
        with open(filename, 'rb') as f:
            print(f"Відправка файлу {filename}..")
            data = f.read(1024)
            while data:
                sock.send(data)
                data = f.read(1024)
        print("Відправка завершена")
    except FileNotFoundError:
        print("Помилка: Файл не знайдено в папці з програмою")

    sock.close()

if __name__ == "__main__":
    send_file()