import csv
import datetime
import time
from plyer import notification

tasks = []

def display_menu():
    print("===== To-Do List =====")
    print("1. Add a task")
    print("2. View tasks and reminders")
    print("3. Mark task as completed")
    print("4. Exit")

def save_tasks_to_csv():
    with open('tasks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Description', 'Reminder Text', 'Reminder Date', 'Reminder Time', 'Completed'])
        for task in tasks:
            writer.writerow([task['description'], task['reminder_text'], task['reminder_date'], task['reminder_time'], task['completed']])

def load_tasks_from_csv():
    tasks.clear()
    try:
        with open('tasks.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append({
                    'description': row['Description'],
                    'reminder_text': row['Reminder Text'],
                    'reminder_date': row['Reminder Date'],
                    'reminder_time': row['Reminder Time'],
                    'completed': row['Completed'] == 'True'
                })
    except FileNotFoundError:
        pass

def add_task():
    task = input("Enter task description: ")
    reminder_text = input("Enter the reminder text: ")
    date_str = input("Enter the reminder date (YYYY-MM-DD): ")
    time_str = input("Enter the reminder time (HH:MM): ")
    tasks.append({
        "description": task,
        "reminder_text": reminder_text,
        "reminder_date": date_str,
        "reminder_time": time_str,
        "completed": False
    })
    print("Task added successfully!")

def view_tasks_and_reminders():
    if not tasks:
        print("No tasks found.")
    else:
        while True:
            current_datetime = datetime.datetime.now()
            print("Tasks and Reminders:")
            for index, task in enumerate(tasks, start=1):
                status = "Completed" if task["completed"] else "Incomplete"
                reminder_datetime = datetime.datetime.strptime(task['reminder_date'] + " " + task['reminder_time'], "%Y-%m-%d %H:%M")
                time_difference = reminder_datetime - current_datetime
                remaining_time = time_difference.total_seconds()
                if remaining_time <= 0:
                    print(f"{index}. {task['description']} - {status} (Reminder time passed)")
                else:
                    remaining_hours = int(remaining_time / 3600)
                    remaining_minutes = int(remaining_time / 60)
                    print(f"{index}. {task['description']} - {status} (Reminder in {remaining_hours} hours, {remaining_minutes} minutes)")
                    notify_task_reminder(task['description'], status, remaining_hours, remaining_minutes)
            choice = input("Enter 'm' to return to the program or any other key to refresh: ")
            if choice == 'm':
                break

def notify_task_reminder(description, status, hours, minutes):
    notification.notify(
        title="Task Reminder",
        message=f"{description} - {status} (Reminder in {hours} hours, {minutes} minutes)",
        timeout=30  # Durasi notifikasi dalam detik
    )

def mark_task_as_completed():
    view_tasks_and_reminders()
    task_number = int(input("Enter the task number to mark as completed: "))
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        print("Task marked as completed!")
    else:
        print("Invalid task number.")

def main():
    load_tasks_from_csv()

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            add_task()
            save_tasks_to_csv()
        elif choice == "2":
            view_tasks_and_reminders()
        elif choice == "3":
            mark_task_as_completed()
            save_tasks_to_csv()
        elif choice == "4":
            save_tasks_to_csv()
            break
        else:
            print("Invalid choice. Please try again.")

        print()

if __name__ == "__main__":
    main()
