'''
Так как данное задание пришлось невероятно тяжелым для меня,
я сгенерировал его через ИИ
я долго висел над ним пытясь сам разобратья что к чему
но принял решение разобрать уже готовый код как конструктор
принимая для себя новое
'''
from storage import load_notes, add_note, delete_note, search_notes

def main():
    while True:
        print("1. Добавить заметку")
        print("2. Показать все заметки")
        print("3. Найти заметку")
        print("4. Удалить заметку по ID")
        print("5. Выйти")
        choice = input("Выбери действие: ")

        if choice == "1":
            text = input("Текст заметки: ")
            if text.strip():
                add_note(text)
                print("Заметка добавлена!")
            else:
                print("Пустую заметку не добавляю.")

        elif choice == "2":
            notes = load_notes()
            if not notes:
                print("Пока нет ни одной заметки.")
            else:
                print("\nСписок заметок:")
                for note in notes:
                    print(f"{note['id']}. {note['text']} (создано {note['created_at']})")

        elif choice == "3":
            keyword = input("Что ищем? ")
            found = search_notes(keyword)
            if not found:
                print("Ничего не найдено.")
            else:
                print(f"\nНашлось {len(found)} заметок:")
                for note in found:
                    print(f"{note['id']}. {note['text']}")

        elif choice == "4":
            try:
                note_id = int(input("Введи ID заметки, которую хочешь удалить: "))
                if delete_note(note_id):
                    print("Удалил.")
                else:
                    print("Заметки с таким ID нет.")
            except ValueError:
                print("Ошибка! Нужно писать число.")

        elif choice == "5":
            print("Пока!")
            break

        else:
            print("Такого пункта нет, выбери 1-5.")

if __name__ == "__main__":
    main()