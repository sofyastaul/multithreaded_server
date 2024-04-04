import socket    #предоставляет возможность работать с сетевыми сокетами, что позволяет создавать клиент-серверные сетевые приложения
import threading     #предоставляет инструменты для работы с потоками (threads) в многопоточных программах
import json

def data_receiving(message, client_socket, addr):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message += data

        if message.lower() == 'отключение от сервера':
            print("Отключение клиента:", addr)
            client_socket.send("Разрыв соединения с сервером".encode())
            client_socket.close()
            break
        client_socket.send("Сообщение успешно обработано сервером".encode())

        return json.loads(message.decode())



def handle_client(client_socket, addr):
    print("Подключение клиента:", addr)

    message = data_receiving(b'', client_socket, addr)

    print("Полученное сообщение:", message)
    ans = json.dumps(message).encode()
    client_socket.send(ans)
    print("Отправленное сообшение:", ans)

    client_socket.close()    #используется для закрытия сокета после завершения работы с ним

# Создание TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #создание нового объекта сокета для работы с сетью
                                                                     #первый аргумент socket.AF_INET указывает на используемый адресный семейство,
                                                                     #в данном случае IPv4. Второй аргумент socket.SOCK_STREAM указывает на тип сокета,
                                                                     #в данном случае потоковый сокет (TCP)
server_socket.bind(('127.0.0.1', 12353))     #привязка сокета к заданному хосту и порту
server_socket.listen(5)    #используется для установки сокета в режим прослушивания входящих подключений
                           #аргумент 5 обозначает максимальную длину очереди ожидающих подключений.
                           #это значит, что сервер будет принимать до 5 запросов на соединение в ожидании обработки
print("Запуск сервера")

# Начало прослушивания порта
print("Начало прослушивания порта")

while True:
    client_socket, addr = server_socket.accept()    #эта строка принимает входящее соединение от клиента и создает новый сокет client_socket
                                                    #для взаимодействия с этим клиентом,а также сохраняет адрес клиента в переменной addr
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))    #создается новый объект типа Thread из модуля threading.
                                                                                          #этот объект предназначен для выполнения функции handle_client в отдельном потоке
    client_thread.start()    #запуск нового потока

server_socket.close()    #используется для закрытия сокета после завершения работы с ним
print("Остановка сервера")