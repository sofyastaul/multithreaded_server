import socket
import json
# Создание TCP-клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #создание нового объекта сокета для работы с сетью
                                                                     #первый аргумент socket.AF_INET указывает на используемый адресный семейство,
                                                                     #в данном случае IPv4. Второй аргумент socket.SOCK_STREAM указывает на тип сокета,
                                                                     #в данном случае потоковый сокет (TCP)
server_address = ('127.0.0.1', 12353)    #привязка сокета к заданному хосту и порту

print("Соединение с сервером")
client_socket.connect(server_address)    #устанавливает соединение с удаленным сокетом, определенным по параметрам server_address

while True:
    message = input("Введите сообщение для отправки серверу: ")
    client_socket.send(json.dumps(message).encode())    #отправляем ответ серверу в формате json, чтобы можно было передавать массивы
    print(client_socket.recv(4096).decode())# получаем сообщение об успешной обработке отправленного запроса

    data = client_socket.recv(4096).decode()   #получаем ответ от сервера. Метод recv(1024) получает данные от сервера в виде байтов
    received_message = json.loads(data)    #преобразвем данные из json в строку

    if received_message == "Разрыв соединения с сервером":
        print(received_message)
        s = input("Хотите ли вы подключиться к серверу снова? Напишите да/нет: ")
        if s == "да":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #создается новый объект клиентского сокета
            client_socket.connect(server_address)    #устанавливается соединение с сервером, используя адрес server_address
        elif s == "нет":
            client_socket.close()    #используется для закрытия сокета после завершения работы с ним.
                                     #после вызова этого метода, сокет перестает прослушивать входящие соединения
            break
        else:
            print("Вы ввели некорректные данные!")
            client_socket.close()
            break
    else:
        print("Ответ от сервера: ", received_message)