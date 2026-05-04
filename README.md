# CLI Task Tracker

[🌐 Source Code](https://github.com/roland-radionov/CLI-Task-Tracker) | [🪪 License: MIT](LICENSE)

A simple command-line task manager to create, manage, and display your tasks.

## **Features**
- **Global Access:** Run `task-cli` from any directory in your terminal.
- **Persistent Storage:** Tasks are saved in `~/.tasks.json` in your home directory, making them accessible from everywhere.
- **Lightweight:** No heavy databases required, just a simple and fast JSON storage.

## **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/roland-radionov/CLI-Task-Tracker.git
cd CLI-Task-Tracker
```

2. **Install the project:**
```bash
pip install .
```
*Note: If `pip` command is not found, try:*
```bash
python -m pip install .
```

## **Usage**

- **Add a new task:**
```bash
task-cli add "Task description"
```
- **Update or delete tasks (using task ID):**
```bash
task-cli update <id> "New task description"
task-cli delete <id>
```
- **Mark a task status:**
```bash
task-cli mark-in-progress <id>
task-cli mark-done <id>
task-cli mark-todo <id>
```
- **List all tasks:**
```bash
task-cli list
```
- **List tasks by status:**
```bash
task-cli list done
task-cli list todo
task-cli list in-progress
```

## **Tech Stack**
- **Python 3.x**
- **Setuptools** (for installation)
