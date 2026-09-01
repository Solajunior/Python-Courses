import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("daily_data.json")


def load_data():
    if not DATA_FILE.exists():
        return {
            "date": str(datetime.today().date()),
            "tasks": [],
            "notes": [],
            "habits": {
                "water": 0,
                "exercise": False,
                "study": False,
                "sleep": "",
            },
            "focus": "",
        }

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if data.get("date") != str(datetime.today().date()):
            data["date"] = str(datetime.today().date())
            data["tasks"] = []
            data["notes"] = []
            data["habits"] = {
                "water": 0,
                "exercise": False,
                "study": False,
                "sleep": "",
            }
            data["focus"] = ""
            save_data(data)
        return data
    except (json.JSONDecodeError, TypeError, ValueError):
        default = {
            "date": str(datetime.today().date()),
            "tasks": [],
            "notes": [],
            "habits": {
                "water": 0,
                "exercise": False,
                "study": False,
                "sleep": "",
            },
            "focus": "",
        }
        save_data(default)
        return default


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def show_tasks(tasks):
    if not tasks:
        print("  No tasks yet.")
        return

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else "-"
        print(f"  {index}. [{status}] {task['title']}")


def add_task(data):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task cannot be empty.")
        return
    data["tasks"].append({"title": title, "done": False})
    print(f"Task added: {title}")


def mark_task_done(data):
    if not data["tasks"]:
        print("No tasks to complete.")
        return

    show_tasks(data["tasks"])
    try:
        choice = int(input("Choose task number to complete: ")) - 1
        if 0 <= choice < len(data["tasks"]):
            data["tasks"][choice]["done"] = True
            print(f"Completed: {data['tasks'][choice]['title']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def add_note(data):
    note = input("Write a quick note: ").strip()
    if not note:
        print("Note cannot be empty.")
        return
    data["notes"].append({"time": datetime.now().strftime("%H:%M"), "text": note})
    print("Note saved.")


def view_notes(data):
    if not data["notes"]:
        print("  No notes for today.")
        return

    print("\nYour notes:")
    for note in data["notes"]:
        print(f"  [{note['time']}] {note['text']}")


def update_habits(data):
    print("\nHabit tracker")
    print("1. Add water glasses")
    print("2. Toggle exercise")
    print("3. Toggle study")
    print("4. Set sleep time")
    print("5. Back")

    choice = input("Choose: ").strip()

    if choice == "1":
        try:
            amount = int(input("How many glasses of water? "))
            data["habits"]["water"] += amount
            print(f"Water total: {data['habits']['water']} glasses")
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        data["habits"]["exercise"] = not data["habits"]["exercise"]
        print("Exercise status updated.")

    elif choice == "3":
        data["habits"]["study"] = not data["habits"]["study"]
        print("Study status updated.")

    elif choice == "4":
        sleep_time = input("Sleep time (e.g. 10:30 PM): ").strip()
        data["habits"]["sleep"] = sleep_time
        print("Sleep time saved.")


def set_focus(data):
    focus = input("What is your main focus today? ").strip()
    data["focus"] = focus
    print("Focus saved.")


def show_summary(data):
    print("\n=== Daily Summary ===")
    print(f"Date: {data['date']}")
    print(f"Focus: {data['focus'] or 'No focus set'}")
    print(f"Water: {data['habits']['water']} glasses")
    print(f"Exercise: {'Yes' if data['habits']['exercise'] else 'No'}")
    print(f"Study: {'Yes' if data['habits']['study'] else 'No'}")
    print(f"Sleep: {data['habits']['sleep'] or 'Not set'}")
    print("\nTasks:")
    show_tasks(data["tasks"])
    print("\nNotes:")
    view_notes(data)


def main():
    print("Daily Data Helper")
    print("=================")
    data = load_data()

    while True:
        print("\n1. Add task")
        print("2. Mark task done")
        print("3. Add note")
        print("4. View notes")
        print("5. Habit tracker")
        print("6. Set focus")
        print("7. Daily summary")
        print("8. Save and exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(data)
        elif choice == "2":
            mark_task_done(data)
        elif choice == "3":
            add_note(data)
        elif choice == "4":
            view_notes(data)
        elif choice == "5":
            update_habits(data)
        elif choice == "6":
            set_focus(data)
        elif choice == "7":
            show_summary(data)
        elif choice == "8":
            save_data(data)
            print("Your daily data has been saved. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-8.")

        save_data(data)


if __name__ == "__main__":
    main()
