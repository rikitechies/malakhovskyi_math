import socket

def process_expression(expression):
    try:
        result = eval(expression)
        return f"Результат: {result}"
    except Exception as e:
        return "Помилка синтаксису чи ділення на нуль"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    
    print("Сервер запущено")
    
    conn, addr = server_socket.accept()
    
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data or data.lower() == 'exit':
            break
        
        print(f"Отримано вираз: {data}")
        response = process_expression(data)
        conn.send(response.encode('utf-8'))
    
    conn.close()

if __name__ == "__main__":
    start_server()