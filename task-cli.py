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

args = sys.argv
if len(args) < 2:
    sys.exit("Error: You have not specified an action (add, update, delete)")
action = args[1]
tasks_file = "tasks.json"

match action:
    case "add":
        if len(args) < 3:
            sys.exit("Error: The task text was not entered.")

        task = get_task(args[2])
        try:
            with open(tasks_file, "r", encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(task)
        try:
            with open(tasks_file, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            print(f"(ID: {task["id"]}) Task added successfully")
        except IOError as e:
            print(f'File write error: {e}')
    
    case "update":
        if len(args) < 4:
            sys.exit("Error: You have not specified the ID and new task text.")
        id = args[2]
        new_description = args[3]

        try:
            with open(tasks_file, "r", encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            sys.exit("Error: You haven't added any tasks yet.")
        except json.JSONDecodeError as e:
            sys.exit(e)
        
        for task in data:
            if task['id'] == id:
                task['description'] = new_description
                task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M')

        try:
            with open(tasks_file, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            print(f"(ID: {id}) The task description has been successfully changed to \"{new_description}\"")
        except IOError as e:
            print(f'File write error: {e}')

    case "delete":
        if len(args) < 3:
            sys.exit("Error: The ID of the task to be deleted is not specified.")

        id = args[2]
        try:
            with open(tasks_file, "r", encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            sys.exit("Error: You haven't added any tasks yet.")
        except json.JSONDecodeError as e:
            sys.exit(e)

        new_data = [task for task in data if task["id"] != id]
        if len(new_data) == len(data):
            sys.exit(f"There is no task with (ID: {id})")

        try:
            with open(tasks_file, "w", encoding='utf-8') as file:
                json.dump(new_data, file, indent=2, ensure_ascii=False)
            print(f"(ID: {id}) The task has been successfully deleted")
        except IOError as e:
            print(f'File write error: {e}')

    case _:
        print("Valid actions - add, update, delete")

