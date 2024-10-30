import sys
import json
import os
from datetime import datetime

# Constants for the JSON file location
TASKS_FILE = "tasks.json"

# Ensure the tasks file exists, or create it
def initialize_task_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)  # Initialize with an empty list

# Load tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f) or []  # Ensure it defaults to an empty list if the file is empty
    return []

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Generate a unique ID for new tasks
def generate_task_id(tasks):
    if tasks:
        return max(task["id"] for task in tasks) + 1
    return 1

# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = generate_task_id(tasks)
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Update an existing task description
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) updated successfully")
            return
    print(f"Task (ID: {task_id}) not found")

# Delete a task by ID
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task (ID: {task_id}) deleted successfully")

# Mark a task as "in progress"
def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) marked as in-progress")
            return
    print(f"Task (ID: {task_id}) not found")

# Mark a task as "done"
def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) marked as done")
            return
    print(f"Task (ID: {task_id}) not found")

# List tasks based on status
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    for task in tasks:
        print(f"[ID: {task['id']}] {task['description']} - {task['status']} (Created: {task['createdAt']}, Updated: {task['updatedAt']})")

# Command-line argument handler
def main():
    initialize_task_file()
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        return

    command = sys.argv[1]
    if command == "add" and len(sys.argv) >= 3:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) >= 4:
        update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "delete" and len(sys.argv) >= 3:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) >= 3:
        mark_in_progress(int(sys.argv[2]))
    elif command == "mark-done" and len(sys.argv) >= 3:
        mark_done(int(sys.argv[2]))
    elif command == "list":
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print("Invalid command. Try 'add', 'update', 'delete', 'mark-in-progress', 'mark-done', or 'list'.")

if __name__ == "__main__":
    main()

