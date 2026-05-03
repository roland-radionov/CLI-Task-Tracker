#!/usr/bin/env python3

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
        sys.exit("Error: Missing task description")

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
    
    found = False
    for task in data:
        if task['id'] == id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            found = True
            break
    
    if not found:
        sys.exit(f"Error: Task with ID {id} not found.")

    if save_tasks(tasks_file, data):
        print(f"(ID: {id}) Task description updated successfully to \"{new_description}\"")

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

def mark_task(args: list[str], tasks_file: str, new_status: str):
    if len(args) < 3:
        sys.exit("Error: The ID of the task to be marked is not specified.")

    id = args[2]
    data = load_tasks(tasks_file)
    if not data:
        sys.exit("Error: You haven't added any tasks yet.")

    found = False
    for task in data:
        if task['id'] == id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            found = True
            break

    if not found:
        sys.exit(f"Error: Task with ID {id} not found.")
    
    if save_tasks(tasks_file, data):
        print(f"(ID: {id}) Task marked as \'{new_status}\' successfully")

def list_tasks(args: list[str], tasks_file: str):
    if len(args) > 3:
        sys.exit("Error: Too many arguments")

    data = load_tasks(tasks_file)
    if not data:
        sys.exit("No tasks found.")
    
    status_filter = args[2] if len(args) == 3 else None
    tasks_to_show = [t for t in data if status_filter is None or t['status'] == status_filter]
    for task in tasks_to_show:
        print(f"(ID: {task['id']})\n"
              f"  Description: {task['description']}\n"
              f"  Status: {task['status']}\n"
              f"  Created: {task['createdAt']}\n"
              f"  Updated: {task['updatedAt']}\n")
    
    print(f"<{'-'*10} Total tasks: {len(tasks_to_show)} {'-'*10}>")

def main():
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
        
        case "mark-in-progress":
            mark_task(args, tasks_file, "in-progress")
        
        case "mark-todo":
            mark_task(args, tasks_file, "todo")
        
        case "mark-done":
            mark_task(args, tasks_file, "done")

        case "list":
            list_tasks(args, tasks_file)

        case _:
            print("Valid actions: add, update, delete, list, mark-todo, mark-in-progress, mark-done")

if __name__ == "__main__":
    main()