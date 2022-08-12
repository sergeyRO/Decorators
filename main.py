from datetime import datetime

def logger(path):
    def decorator(other_function):
        def log(*args):
            function = other_function(*args)
            print(f"Дата и время вызова функции: {datetime.now()}")
            print(f"Функция: {other_function}")
            print("Аргументы: ", *args)
            print(f'Результат: {function}')
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f"{dict(data=f'{datetime.now()}', func=other_function, args=args, result=function)}\n")
            return function
        return log
    return decorator

@logger('./logs/search_people.txt')
# Поиск владельца по номеру документа
def search_people(number_doc):
    for doc in documents:
        if doc['number'] == number_doc:
            return doc['name']

@logger('./logs/search_shelf.txt')
# Поиск документа на полке
def search_shelf(number_doc):
    for key, docs in directories.items():
        if number_doc in docs:
            string = f"Документ находится на полке {key}"
            return string
    string = f"Данный документ отсутствует!"
    return string

@logger('./logs/search_list.txt')
# Список всех документов
def search_list():
    for doc in documents:
        print(f"{doc['type']} \"{doc['number']}\" \"{doc['name']}\"")
    return documents

@logger('./logs/add_doc.txt')
# Добавление документа
def add_doc(number_doc, type_doc, owner, shelf):
    val = directories.get(shelf, None)
    if val != None:
        documents.append(dict(type=type_doc, number=number_doc, name=owner))
        val.append(number_doc)
        directories[shelf] = val
        result = f"Документ добавлен в список и на полку {shelf}"
        return result
    else:
        result = f"Полка {shelf} отсутствует! Документ не добавлен!"
        return result

@logger('./logs/drop_doc.txt')
# Удаление документа
def drop_doc(number_doc):
    document = False
    directory = False
    for doc in documents:
        if doc['number'] == number_doc:
            documents.remove(doc)
            document = True
            break
    for key, docs in directories.items():
        if number_doc in docs:
            docs.remove(number_doc)
            directory = True
            break
    if document and directory:
        result = "Документ удалён из списков и с полки"
        return result
    else:
        if document and not directory:
            result = "Документ отсутствует на полке, но удалён из списка"
        elif not document and directory:
            result = "Документ отсутствует в списке, но удалён с полки"
        else:
            result = "Документ не существует"
        return result

@logger('./logs/modify_doc.txt')
# Перемещение документа
def modify_doc(number_doc, shelf):
    document = False
    if shelf in directories:
        for key, docs in directories.items():
            if number_doc in docs:
                docs.remove(number_doc)
                document = True
                directories[shelf].append(number_doc)
                break
        if not document:
            res = f"Документ {number_doc} не существует!"
            return res
        else:
            res = f"Документ {number_doc} перенесён на полку {shelf}"
            return res
    else:
        res = f"Полка {shelf} не существует!"
        return res

@logger('./logs/add_shelf.txt')
# Перемещение документа
def add_shelf(shelf):
    if shelf in directories:
        res = f"Полка {shelf} существует!"
        return res
    else:
        directories.setdefault(shelf, [])
        res = f"Полка {shelf} добавлена!"
        return res

@logger('./logs/exit.txt')
# Выход из программы
def command_exit():
    res = "EXIT"
    return res

if __name__ == '__main__':
    documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
    ]

    directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006'],
        '3': []
    }

    # Ввод
    while True:
        command = input("Введите команду: ")
        if command == "p":
            number_doc = input("Введите номер документа: ")
            print(search_people(number_doc))
        elif command == "s":
            number_doc = input("Введите номер документа: ")
            print(search_shelf(number_doc))
        elif command == "l":
            search_list()
        elif command == "a":
            number_doc = input("Введите номер документа: ")
            type_doc = input("Введите тип документа: ")
            owner = input("Введите владельца: ")
            shelf = input("Введите номер полки для хранения: ")
            print(add_doc(number_doc, type_doc, owner, shelf))
            print(directories)
        elif command == "d":
            number_doc = input("Введите номер документа: ")
            print(drop_doc(number_doc))
            print(directories)
            print(documents)
        elif command == "m":
            number_doc = input("Введите номер документа: ")
            shelf = input("Введите номер полки для хранения: ")
            print(modify_doc(number_doc, shelf))
            print(directories)
        elif command == "as":
            shelf = input("Введите номер полки для хранения: ")
            print(add_shelf(shelf))
            print(directories)
        elif command == "q":
            print(command_exit())
            quit()
        else:
            print("Несуществующая команда!")