import csv
import datetime
import time
import threading
from plyer import notification
from tabulate import tabulate
import matplotlib.pyplot as plt
from operator import itemgetter

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
    while True:
        try:
            date_str = input("Enter the reminder date (YYYY-MM-DD): ")
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    while True:
        try:
            time_str = input("Enter the reminder time (HH:MM): ")
            datetime.datetime.strptime(time_str, "%H:%M")
            break
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")
    reminder_datetime = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")        
    tasks.append({
        "description": task,
        "reminder_text": reminder_text,
        "reminder_date": date_str,
        "reminder_time": time_str,
        "completed": False
    })
    print("Task added successfully!")
    threading.Thread(target=schedule_notification, args=(tasks[-1], reminder_datetime)).start()

def schedule_notification(task, reminder_datetime):
    current_datetime = datetime.datetime.now()
    time_difference = reminder_datetime - current_datetime
    notification_time = time_difference.total_seconds() - 3600
    notification_time = time_difference.total_seconds() - 86400

    if notification_time > 0:
        time.sleep(notification_time)
        notification.notify(
            title = "Task Reminder",
            message = f"{task['description']} - {task['reminder_text']}",
            timeout=30
        )

def display_tasks_table():
    headers = ['Task Number', 'Reminder Text', 'Reminder Date', 'Reminder Time', 'Completed']
    rows = []
    sorted_tasks = sorted(tasks, key=lambda x: (x['reminder_date'], x['reminder_time']))  # Mengurutkan berdasarkan tanggal dan waktu

    for index, task in enumerate(sorted_tasks, start=1):
        status = "Completed" if task["completed"] else "Incomplete"
        rows.append([index, task['description'], task['reminder_text'], task['reminder_date'], task['reminder_time'], status])

    table = tabulate(rows, headers=headers, tablefmt='grid')
    print(table)

def view_tasks_and_reminders():
    input("Press Enter to continue...")
    display_menu()

def mark_task_as_completed():
    display_tasks_table()
    while True:
        try:
            task_number = int(input("Enter the task number to mark as completed: "))
            sorted_tasks = sorted(tasks, key=lambda x: (x['reminder_date'], x['reminder_time']))  # Mengurutkan berdasarkan tanggal dan waktu
            if 1 <= task_number <= len(sorted_tasks):
                sorted_tasks[task_number - 1]["completed"] = True
                tasks[tasks.index(sorted_tasks[task_number - 1])]["completed"] = True
                print("Task marked as completed!")
                break
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")


def calculate_task_completion_percentage():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks

    if total_tasks == 0:
        complete_percentage = 0
        incomplete_percentage = 0
    else:
        complete_percentage = (completed_tasks / total_tasks) * 100
        incomplete_percentage = (incomplete_tasks / total_tasks) * 100

    return complete_percentage, incomplete_percentage

def display_task_completion_graph(complete_percentage, incomplete_percentage):
    labels = ['Complete', 'Incomplete']
    sizes = [complete_percentage, incomplete_percentage]
    colors = ['#1f77b4', '#ff7f0e']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Task Completion')
    plt.show()

def check_overdue_tasks():
    current_datetime = datetime.datetime.now()
    overdue_tasks = [task for task in tasks if not task['completed'] and datetime.datetime.strptime(task['reminder_date'] + ' ' + task['reminder_time'], "%Y-%m-%d %H:%M") < current_datetime]
    if overdue_tasks:
        for task in overdue_tasks:
            notification.notify(
                title="Overdue Task",
                message=f"{task['description']} - {task['reminder_text']}",
                timeout=30
            )

def to_do_task():
    current_datetime = datetime.datetime.now()
    for index, task in enumerate(tasks, start=1):
        if not task['completed']:
            status = "Incomplete"
            reminder_datetime = datetime.datetime.strptime(task['reminder_date'] + " " + task['reminder_time'], "%Y-%m-%d %H:%M")
            time_difference = reminder_datetime - current_datetime
            remaining_time = time_difference.total_seconds()
            if remaining_time <= 0:
                pass
            else:
                remaining_hours = int(remaining_time / 3600)
                remaining_minutes = int(remaining_time / 60 - remaining_hours * 60)
                notify_task_reminder(task['description'], status, remaining_hours, remaining_minutes)


def notify_task_reminder(description, status, hours, minutes):
    notification.notify(
        title="Task Reminder",
        message=f"{description} - {status} (Reminder in {hours} hours, {minutes} minutes)",
        timeout=30  # Durasi notifikasi dalam detik
    )

def main():
    load_tasks_from_csv()

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            add_task()
            save_tasks_to_csv()
        elif choice == "2":
            display_tasks_table()
            view_tasks_and_reminders()
            complete_percentage, incomplete_percentage = calculate_task_completion_percentage()
            print("-----Task Completion-----")
            print(f"Complete: {complete_percentage:.2f}%")
            print(f"Incomplete: {incomplete_percentage:.2f}%")
            display_task_completion_graph(complete_percentage, incomplete_percentage)
            check_overdue_tasks()
            to_do_task()
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
