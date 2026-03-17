import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    print("Введіть арифметичний вираз або 'exit' :")
    
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))
        
        if message.lower() == 'exit':
            break
        
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Відповідь сервера: {data}")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()