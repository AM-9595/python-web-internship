from services import show_task, add_task, delete_task, change_task, find_task

def show_tasks(tasks):
    if not tasks:
        print("Нет задач.")
        return
    for task in tasks:
        print(f"ID: {task['id']}")
        print(f"Название: {task['title']}")
        print(f"Описание: {task['description']}")
        print(f"Статус: {task['status']}")
        print(f"Создана: {task['created_at'][:10]}")
        print("-" * 30)

def main():
    while True:
        print("\n1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Изменить статус")
        print("4. Удалить задачу по ID")
        print("5. Найти задачу по тексту")
        print("0. Выйти")
        choice = input("Выбери действие: ").strip()

        if choice == "1":
            title = input("Введите название задачи: ").strip()
            if not title:
                print("Название не может быть пустым.")
                continue
            description = input("Введите описание: ").strip()
            if not description:
                description = "(без описания)"
            new_task = add_task(title, description)
            if new_task:
                print(f"Задача добавлена с ID {new_task['id']}")
            else:
                print("Ошибка при добавлении.")

        elif choice == "2":
            tasks = show_task()
            show_tasks(tasks)

        elif choice == "3":
            task_id = input("Введите ID задачи: ").strip()
            new_status = input("Новый статус (new/in_progress/done): ").strip().lower()
            if change_task(task_id, new_status):
                print("Статус обновлён.")
            else:
                print("Ошибка: задача не найдена или статус недопустим.")

        elif choice == "4":
            task_id = input("Введите ID задачи для удаления: ").strip()
            confirm = input("Вы уверены? (y/n): ").strip().lower()
            if confirm == "y":
                if delete_task(task_id):
                    print("Задача удалена.")
                else:
                    print("Задача не найдена.")

        elif choice == "5":
            text = input("Введите текст для поиска: ").strip()
            if not text:
                print("Текст не введён.")
                continue
            found = find_task(text)
            if found:
                print(f"Найдено {len(found)} задач:")
                show_tasks(found)
            else:
                print("Ничего не найдено.")

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()