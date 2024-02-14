import time
import json

def save(notes):
    with open("savedNotes.json", "w", encoding="utf-8") as doc:
        doc.write(json.dumps(notes, ensure_ascii=False))

def load():
    try:
        print("<---Notes--->")
        with open("savedNotes.json", "r", encoding="utf-8") as doc:
            notes = json.load(doc)
        print("Заметки загружены\n")
        save(notes)
        return notes
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Ошибка при загрузке файла JSON. Файл поврежден или имеет неверный формат.")
        return {}

def showAll(notes):
    if(notes):
        print("Ваши заметки:")
        for id, data in notes.items():
            print(f"№ {data.get('id', 'N/A')}; {data.get('titleNote', 'N/A')}; Дата: {data.get('currentDate', 'N/A')}")
        note_id = input("Хотите открыть свою заметку? Введите ID. Хотите назад? Введите \"no\": ")
        if note_id.lower() != "no":
            show_note_body(notes, note_id)
    else:
        print("У вас нет заметок.")

def showDate(notes):
    if(notes):
        print("Введите диапазон дат, чтобы отфильтровать заметки:")
        start_date = input("Введите начальную дату (формат: ДД-ММ-ГГГГ): ")
        end_date = input("Введите конечную дату (формат: ДД-ММ-ГГГГ): ")

        try:
            start_time = time.strptime(start_date, "%d-%m-%Y")
            end_date = time.strptime(end_date, "%d-%m-%Y")
            if end_date < start_time:
                print("Ошибка: Начальная дата позже конечной даты.")
                return
        except ValueError:
            print("Ошибка: Неверный формат даты.")
            return

        print("Ваши заметки:")
        for id, data in notes.items():
            note_data = time.strptime(data.get('currentDate'), "%a %b %d %H:%M:%S %Y")
            if start_time <= note_data <= end_date:
                print(f"№ {data.get('id', 'N/A')};"
                      f" {data.get('titleNote', 'N/A')};"
                      f" Дата: {data.get('currentDate', 'N/A')}")

        note_id = input("Хотите открыть свою заметку? Введите ID. Хотите назад? Введите \"no\": ")
        if note_id.lower() != "no":
            show_note_body(notes, note_id)
    else:
        print("У вас нет заметок.")

def show_note_body(notes, note_id):
    try:
        if note_id in notes:
            print(f"Заметка № {note_id}: {notes[note_id]['titleNote']}")
            print(notes[note_id]['bodyNote'])
            print()
        else:
            print("Заметка с таким ID не найдена.\n")
    except ValueError:
        print("Неверный ввод.\n")


def add(notes, id_counter):
    titleNote = input("Введите заголовок заметки: ")
    bodyNote = input("Введите свою заметку:\n")
    currentDate = time.ctime(time.time())

    entry_id = str(id_counter)
    for key, value in notes.items():
        if 'id' in value and value['id'] == id_counter:
            entry_id = str(id_counter + 1)

    notes[entry_id] = {'id': entry_id, 'titleNote': titleNote, 'bodyNote': bodyNote, 'currentDate': currentDate}
    save(notes)

def delete(notes):
    if (notes):
        note_id = input("Введите ID заметки для ее удаления: ")
        try:
            if note_id in notes:
                del notes[note_id]
                print("Ваша заметка была удалена.\n")
                save(notes)
            else:
                print("Заметка с таким ID не была найдена.\n")
        except ValueError:
            print("Неверный ввод. Введите ID заметки.")
    else:
        print("У вас нет заметок.")


def change(notes):
    if (notes):
        note_id = input("Введите ID заметки для ее изменения: ")
        try:
            if note_id in notes:
                new_title = input("Введите новый заголовок своей заметки: ")
                new_body = input("Введите свою новую заметку:\n")
                notes[note_id]['titleNote'] = new_title
                notes[note_id]['bodyNote'] = new_body
                notes[note_id]['currentDate'] = time.ctime(time.time())
                print("Заметка успешно изменена.\n")
                save(notes)
            else:
                print("Заметка с таким ID не найдена.\n")
        except ValueError:
            print("Неверный ввод. Введите ID заметки.")
    else:
        print("У вас нет заметок.")

notes = load()
id_counter = len(notes) + 1

info = ('Вам доступны следующие команды: \n'
        'load - загружает заметки из файла\n'
        'all - показывает все заметки\n'
        'date - показывает заметки созданные, в указанных датах\n'
        'info - показывает информацию по командам программы\n'
        'delete - удаляет заметку с выбранным ID\n'
        'change - изменяет заметку\n'
        'exit - выход из программы')

while True:
    command = input("Введите одну из команд: info, load, all, date, add, delete, change, exit\n")

    if command == "exit":
        print("До скорой встречи!")
        break

    elif command == "info":
        print(info)

    elif command == "load":
        notes = load()

    elif command == "all":
        showAll(notes)

    elif command == "date":
        showDate(notes)

    elif command == "add":
        add(notes, id_counter)
        id_counter += 1

    elif command == "delete":
        delete(notes)

    elif command == "change":
        change(notes)

    else:
        print('Вы ввели неверную команду! Для списка команд обратитесь к "info"!')