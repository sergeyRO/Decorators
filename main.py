def logger(other_function):
    def log(*args, **kwargs):
        function = other_function(*args, **kwargs)

        print(f"Функция {other_function} Результат {other_function(*args, **kwargs)}")
        print("Аргументы: ", *args, **kwargs)
        return function
    return log


@logger
# Поиск владельца по номеру документа
def search_people(number_doc):
    for doc in documents:
        if doc['number'] == number_doc:
            return doc['name']


@logger
# Поиск документа на полке
def search_shelf(number_doc):
    for key, docs in directories.items():
        if number_doc in docs:
            print(f"Документ находится на полке {key}")
            break
        else:
            print("Документ отсутствует на какой-либо полке!")
    return None


@logger
# Список всех документов
def search_list():
    for doc in documents:
        print(f"{doc['type']} \"{doc['number']}\" \"{doc['name']}\"")


@logger
# Добавление документа
def add_doc(number_doc, type_doc, owner, shelf):
    val = directories.get(shelf, None)
    if val != None:
        documents.append(dict(type=type_doc, number=number_doc, name=owner))
        val.append(number_doc)
        directories[shelf] = val
        print(f"Документ добавлен в список и на полку {shelf}")
    else:
        print(f"Полка {shelf} отсутствует! Документ не добавлен!")
    print(directories)


@logger
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
        print("Документ удалён из списков и с полки")
    else:
        if document and not directory:
            print("Документ отсутствует на полке, но удалён из списка")
        elif not document and directory:
            print("Документ отсутствует в списке, но удалён с полки")
        else:
            print("Документ не существует")


@logger
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
            print(f"Документ {number_doc} не существует!")
        else:
            print(f"Документ {number_doc} перенесён на полку {shelf}")
    else:
        print(f"Полка {shelf} не существует!")


@logger
# Перемещение документа
def add_shelf(shelf):
    if shelf in directories:
        print(f"Полка {shelf} существует!")
    else:
        directories.setdefault(shelf, [])
        print(f"Полка {shelf} добавлена!")


@logger
# Выход из программы
def command_exit(*args, **kwargs):
    quit()


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
            search_shelf(number_doc)
        elif command == "l":
            search_list()
        elif command == "a":
            number_doc = input("Введите номер документа: ")
            type_doc = input("Введите тип документа: ")
            owner = input("Введите владельца: ")
            shelf = input("Введите номер полки для хранения: ")
            add_doc(number_doc, type_doc, owner, shelf)
        elif command == "d":
            number_doc = input("Введите номер документа: ")
            drop_doc(number_doc)
        elif command == "m":
            number_doc = input("Введите номер документа: ")
            shelf = input("Введите номер полки для хранения: ")
            modify_doc(number_doc, shelf)
        elif command == "as":
            shelf = input("Введите номер полки для хранения: ")
            add_shelf(shelf)
        elif command == "q":
            command_exit()
        else:
            print("Несуществующая команда!")
