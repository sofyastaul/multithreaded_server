import socket
import json

server_address = ('127.0.0.1', 12360)
print("Соединение с сервером")

#Основной цикл программы для взаимодействия с сервером
while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #создание нового объекта сокета для работы с сетью
                                                                          #первый аргумент socket.AF_INET указывает на используемый адресный семейство,
                                                                          #в данном случае IPv4. Второй аргумент socket.SOCK_STREAM указывает на тип сокета,
                                                                          #в данном случае потоковый сокет (TCP)
    client_socket.connect(server_address)
    client_socket.send("Сохранить информацию о текущих файлах в директории".encode())
    action = input("Что вы хотите сделать? \n 1. Установить новую корневую папку \n 2. Получить информацию о файлах корневой папке\n 3. Разорвать соединение с сервером \nВвод: ")

    if action == "1":
        client_socket.send("Установить новую корневую папку".encode())
        new_folder = input("Введите полный путь новой папки: ")  # Запрашиваем новую папку у пользователя
        client_socket.send(new_folder.encode())  #Отправляем новую папку на сервер
        print(client_socket.recv(1024).decode())  #Получаем ответ от сервера после отправки новой папки. Метод recv(1024) получает данные от сервера в виде
                                                  #байтов, а метод decode() преобразует эти байты в строку для вывода на экран

    elif action == "2":
        client_socket.send("Получить информацию о файлах корневой папке".encode())
        response = b""  #Создается пустой байтовый объект response, который будет хранить ответ от сервера
        while True:
            data = client_socket.recv(4096)  # Получаем данные от сервера
            response += data  # Добавляем полученные данные к ответу
            if len(data) < 4096:  # Проверяем, были ли получены все данные
                break
        files_info = json.loads(response.decode())  #Данные, полученные от сервера и сохраненные в байтовом объекте response,
                                                    #десериализуются из формата JSON в словарь Python с помощью метода json.loads()
                                                    #Метод decode() используется для преобразования байтов в строку перед десериализацией
        for file_path, file_info in files_info.items():
            print(file_path, file_info)  # Выводим информацию о файлах на экран

    elif action == "3":
        client_socket.close()
        print("Разрыв соединения с сервером")
        s = input("Хотите ли вы подключиться к серверу снова? Напишите да/нет: ")
        if s == "да":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создается новый объект клиентского сокета
            client_socket.connect(server_address)  # устанавливается соединение с сервером, используя адрес server_address
        elif s == "нет":
            client_socket.close()  # используется для закрытия сокета после завершения работы с ним.
            # после вызова этого метода, сокет перестает прослушивать входящие соединения
            break
        else:
            print("Вы ввели некорректные данные!")
            client_socket.close()
            break

    else:
        print("Вы ввели некорректное значение! Попробуйте заново!")
