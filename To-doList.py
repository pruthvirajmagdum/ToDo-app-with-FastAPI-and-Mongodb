from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["tasks"]

def add_task(title):
    task = {
        "title": title,
        "date_created": datetime.now().strftime("%d-%m-%Y"),
        "time": datetime.now().strftime("%I:%M %p"),
        "status": "pending",
    }
    collection.insert_one(task)
    print("Task added!")

def view_tasks():
    tasks = collection.find()
    print("\n Your To-Do List:")
    for task in tasks:
        print(f"-ID: {task['_id']},  Task: {task['title']} ,  created at: {task["date_created"]},  Time: {task["time"]},  (Status: {task['status']})")

def mark_done(title):
    result = collection.update_one({"title": title} ,{"$set": {"status": "done"}})
    if result.modified_count:
        print("Task marked as done.")
    else:
        print("Task not found.")

def delete_task(title):
    result = collection.delete_one({"title": title})
    if result.deleted_count:
        print("Task deleted.")
    else:
        print("Task not found.")

def menu():
    while True:
        print("\n=== To-Do Menu ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            add_task(title)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            title = input("Enter task title to mark as done: ")
            mark_done(title)
        elif choice == "4":
            title = input("Enter task title to delete: ")
            delete_task(title)
        elif choice == "5":
            print("Exit success")
            break
        else:
            print("Invalid choice")

# Run the menu
menu()
