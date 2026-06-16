import uuid
import datetime
import storage

def show_task():
    return storage.load_tasks()

def add_task(title, description):
    tasks = storage.load_tasks()
    task = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "description": description,
        "status": "new",
        "created_at": datetime.datetime.now().isoformat()
    }
    tasks.append(task)
    storage.save_tasks(tasks)
    return task

def delete_task(task_id):
    tasks = storage.load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            storage.save_tasks(tasks)
            return True
    return False

def change_task(task_id, new_status):
    if new_status not in ["new", "in_progress", "done"]:
        return False
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            storage.save_tasks(tasks)
            return True
    return False

def find_task(text):
    tasks = storage.load_tasks()
    text = text.lower()
    return [t for t in tasks if text in t["title"].lower() or text in t["description"].lower()]