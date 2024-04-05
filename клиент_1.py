import socket
import json
import os
import shutil

server_address = ('127.0.0.1', 12360)    #привязка сокета к заданному хосту и порту
print("Соединение с сервером")

def copy_path(src, dst): # три функции для выполнения "инструкций", полученных от сервера
    if os.path.isdir(src):
        shutil.copytree(src, dst)
        return "Скопирована папка: " + str(src) + " в " + str(dst)
    else:
        shutil.copy2(src, dst)
        return "Скопирован файл: " + str(src) + " в " + str(dst)

def remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        return "Удалена папка: " + str(path)
    else:
        os.remove(path)
        return "Удален файл: " + str(path)


def translator(ans):
    if ans[0] == '0':
        return "Папки идентичны"
    elif ans[0] == "1":
        for name in ans[1]:
            src_path = os.path.join(folder1, name)
            dest_path = os.path.join(folder2, name)
            s = copy_path(src_path, dest_path)
            return s
    elif ans[0] == '2':
        for name in ans[1]:
            path = os.path.join(folder2, name)
            s = remove_path(path)
            return s
    else:
        for name in ans[1]:
            src_path = os.path.join(folder1, name)
            dest_path = os.path.join(folder2, name)
            s = copy_path(src_path, dest_path) + "\n"
        for name in ans[2]:
            path = os.path.join(folder2, name)
            s += remove_path(path)
        return s

try:
    folder1 = os.mkdir("Папка 1")
except FileExistsError:
    pass

try:
    folder2 = os.mkdir("Папка 2")
except FileExistsError:
    pass

folder1 = os.getcwd() + "\\Папка 1"
folder2 = os.getcwd() + "\\Папка 2"


while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #создание нового объекта сокета для работы с сетью
                                                                       #первый аргумент socket.AF_INET указывает на используемый адресный семейство,
                                                                       #в данном случае IPv4. Второй аргумент socket.SOCK_STREAM указывает на тип сокета,
                                                                       #в данном случае потоковый сокет (TCP)
    client_socket.connect(server_address)
    action = input("Что вы хотите сделать? \n 1. Сравнить и прировнять содержимое папок \n 2. Разорвать соединение с сервером \nВвод: ")

    if action == "1":
        client_socket.send("Сравнить и прировнять содержимое папок".encode())
        message1 = os.listdir(folder1)
        client_socket.send(json.dumps(message1).encode())

        message2 = os.listdir(folder2)
        client_socket.send(json.dumps(message2).encode())

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode()
        responce = json.loads(response)
        print(f"Ответ от сервера: {response}")
        print(translator(responce))

    elif action == "2":
        client_socket.close()
        print("Разрыв соединения с сервером")
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
        print("Вы ввели некорректное значение! Попробуйте заново!")
