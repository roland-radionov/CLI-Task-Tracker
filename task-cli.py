import sys
import uuid
import json
from datetime import datetime

def get_task(description: str) -> dict:
    return {
        "id": uuid.uuid4().hex[:8],
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "updatedAt": datetime.now().strftime('%Y-%m-%d %H:%M')
    }

def load_tasks(tasks_file: str) -> list[dict]:
    try:
        with open(tasks_file, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        sys.exit(f"Error: JSON syntax error in file {tasks_file}")

def save_tasks(tasks_file: str, data: list[dict]) -> bool:
    try:
        with open(tasks_file, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    
    except IOError as e:
        print(f'File write error: {e}')
        return False

def add(args: list[str], tasks_file: str):
    if len(args) < 3:
        sys.exit("Error: The task text was not entered.")

    task = get_task(args[2])
    data = load_tasks(tasks_file)
    data.append(task)
    if save_tasks(tasks_file, data):
        print(f"(ID: {task["id"]}) Task added successfully")

def update(args: list[str], tasks_file: str):
    if len(args) < 4:
        sys.exit("Error: You have not specified the ID and new task text.")
    id = args[2]
    new_description = args[3]

    data = load_tasks(tasks_file)
    if not data:
        sys.exit("Error: You haven't added any tasks yet.")
        
    for task in data:
        if task['id'] == id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M')

    if save_tasks(tasks_file, data):
        print(f"(ID: {id}) The task description has been successfully changed to \"{new_description}\"")

def delete(args: list[str], tasks_file: str):
    if len(args) < 3:
        sys.exit("Error: The ID of the task to be deleted is not specified.")

    id = args[2]
    data = load_tasks(tasks_file)
    if not data:
        sys.exit("Error: You haven't added any tasks yet.")

    new_data = [task for task in data if task["id"] != id]
    if len(new_data) == len(data):
        sys.exit(f"There is no task with (ID: {id})")

    if save_tasks(tasks_file, new_data):
        print(f"(ID: {id}) The task has been successfully deleted")

args = sys.argv
if len(args) < 2:
    sys.exit("Error: You have not specified an action (add, update, delete)")
action = args[1]
tasks_file = "tasks.json"

match action:
    case "add":
        add(args, tasks_file)
    
    case "update":
        update(args, tasks_file)

    case "delete":
        delete(args, tasks_file)

    case _:
        print("Valid actions - add, update, delete")