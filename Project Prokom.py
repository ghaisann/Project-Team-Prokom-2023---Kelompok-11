from plyer import notification
import datetime
import time


tasks = []

def display_menu():
    print("===== To-Do List =====")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Exit")


def add_task():
    task = input("Enter task description: ")
    tasks.append({"description": task, "completed": False})
    print("Task added successfully!")
 

    reminder_text = input("Enter the reminder text: ")
    date_str = input("Enter the reminder date (YYYY-MM-DD): ")
    time_str = input("Enter the reminder time (HH:MM): ")
    datetime_str = date_str + " " + time_str
    reminder_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    
    current_datetime = datetime.datetime.now()
    time_difference = reminder_datetime - current_datetime
    time_difference_seconds = time_difference.total_seconds()
    
    if time_difference_seconds <= 0:
        print("Invalid reminder time. Please enter a future date and time.")
        return
    
    print("Reminder set successfully!")
    
    # Sleep until the reminder time
    time.sleep(time_difference_seconds)
    
    notification.notify(
        title="Reminder",
        message=reminder_text,
        timeout=10  # Notification display time (in seconds)
    )



def view_tasks():
    if not tasks:
        print("No tasks found.")
    else:
        print("Tasks:")
        for index, task in enumerate(tasks, start=1):
            status = "Completed" if task["completed"] else "Incomplete"
            print(f"{index}. {task['description']} - {status}")




def mark_task_as_completed():
    view_tasks()
    task_number = int(input("Enter the task number to mark as completed: "))
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        print("Task marked as completed!")
    else:
        print("Invalid task number.")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_as_completed()
        elif choice == "4":
             break
        else:
            print("Invalid choice. Please try again.")

        print()

#menjalankan program
if __name__ == "__main__":
    main()

