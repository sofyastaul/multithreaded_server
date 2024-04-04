import socket    #предоставляет возможность работать с сетевыми сокетами, что позволяет создавать клиент-серверные сетевые приложения
import threading     #предоставляет инструменты для работы с потоками (threads) в многопоточных программах
import json
import os

def data_receiving(message, client_socket, addr):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message += data

        return json.loads(message.decode())

def compare_files(file1, file2): #функция сравнения двух файлов
    extra_elements = []

    for el in file2:
        if el in file1:
            file1.remove(el)
        else:
            extra_elements.append(el)

    missing_elements = file1
    # функция высылает клиенту код действия и элементы, с которыми их необходимо произвести. Коды действий:
    # 0 - Массивы полностью совпадают.
    # 1 - Необходимо добавить в массив 2 элементы
    # 2 - Необходимо удалить из массива 2 элементы

    if not missing_elements and not extra_elements:
        return('0')
    elif missing_elements and extra_elements:
        return('1 2', missing_elements, extra_elements)
    elif missing_elements:
        return('1', missing_elements)
    else:
        return('2', extra_elements)

def get_files_info(path):
    files_info = {}  # Создаем пустой словарь для хранения информации о файлах
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_info = {
                'file_name': file,
                'file_path': file_path,
                'file_size': os.path.getsize(file_path)
            }  #Создаем словарь с информацией о файле
            files_info[file_path] = file_info  #Добавляем информацию о файле в словарь
    return files_info

def save_to_json(files_info, output_dir):
    with open(os.path.join(output_dir, 'files_info.json'), 'w', encoding='utf-8') as file:
        json.dump(files_info, file, indent=4, ensure_ascii=False)

def handle_client(client_socket, addr):
    while True:
        command = client_socket.recv(1024).decode()
        if command == "Сравнить и прировнять содержимое папок":
            file1 = data_receiving(b'', client_socket, addr)
            file2 = data_receiving(b'', client_socket, addr)
            answer = compare_files(file1, file2)
            client_socket.send(json.dumps(answer).encode())
        if command == "Сохранить информацию о текущих файлах в директории":
            # Получаем текущую директорию
            current_path = os.getcwd()
            output_dir = current_path
            files_info = get_files_info(current_path)  # Получаем информацию о файлах в текущей директории
            save_to_json(files_info, output_dir)  # Сохраняем информацию о файлах в JSON файл
        if command == "Установить новую корневую папку":
            new_folder = client_socket.recv(1024).decode()  # Получаем новую папку от клиента
            if os.path.exists(new_folder):  # Проверяем существование папки
                os.chdir(new_folder)  # Меняем рабочую директорию
                output_dir = new_folder
                files_info = get_files_info(new_folder)
                save_to_json(files_info, output_dir)
                client_socket.send(f"Новая корневая папка: {new_folder}".encode())
            else:
                client_socket.send("Такой папки не существует".encode())
        if command == "Получить информацию о файлах корневой папке":
            with open(os.path.join(output_dir, 'files_info.json'), 'r', encoding='utf-8') as file:
                files_info = json.load(file)
                json_data = json.dumps(files_info, ensure_ascii=False)    #метод json.dumps() преобразует объект files_info (содержащий информацию
                                                                          #о файлах) в строку в формате JSON. Параметр ensure_ascii=False указывает,
                                                                          #что необходимо разрешить использование символов Unicode в строке JSON (если они есть)
                client_socket.send(json_data.encode())  # Отправляем информацию о файлах клиенту

# Создание TCP-сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #создание нового объекта сокета для работы с сетью
                                                                     #первый аргумент socket.AF_INET указывает на используемый адресный семейство,
                                                                     #в данном случае IPv4. Второй аргумент socket.SOCK_STREAM указывает на тип сокета,
                                                                     #в данном случае потоковый сокет (TCP)
server_socket.bind(('127.0.0.1', 12360))     #привязка сокета к заданному хосту и порту
server_socket.listen(5)    #используется для установки сокета в режим прослушивания входящих подключений
                           #аргумент 5 обозначает максимальную длину очереди ожидающих подключений.
                           #это значит, что сервер будет принимать до 5 запросов на соединение в ожидании обработки
print("Запуск сервера")

while True:
    client_socket, addr = server_socket.accept()    #эта строка принимает входящее соединение от клиента и создает новый сокет client_socket
                                                    #для взаимодействия с этим клиентом,а также сохраняет адрес клиента в переменной addr
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))    #создается новый объект типа Thread из модуля threading.
                                                                                          #этот объект предназначен для выполнения функции handle_client в отдельном потоке
    client_thread.start()    #запуск нового потока

server_socket.close()    #используется для закрытия сокета после завершения работы с ним
print("Остановка сервера")
