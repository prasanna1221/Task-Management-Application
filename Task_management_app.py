import sqlite3
from datetime import datetime, timedelta

class Task:
    def __init__(self, id, description, deadline, status, priority):
        self.id = id
        self.description = description
        self.deadline = deadline
        self.status = status
        self.priority = priority

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', deadline='{self.deadline}', status='{self.status}', priority='{self.priority}')"

def create_table():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Drop the tasks table if it exists to avoid schema conflicts
    #cursor.execute('DROP TABLE IF EXISTS tasks')

    # Create the table with the correct schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT,
            status TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_task(description, deadline, status, priority):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    if deadline:
        deadline = datetime.strptime(deadline, '%d-%m-%Y').strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO tasks (description, deadline, status, priority) VALUES (?, ?, ?, ?)',
                   (description, deadline, status, priority))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    return tasks

def get_tasks_by_status(status):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE status = ?', (status,))
    rows = cursor.fetchall()
    conn.close()
    tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    return tasks

def update_task(task_id, description=None, deadline=None, status=None, priority=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    if not task:
        print("No task found with the given ID.")
        return
    if description:
        cursor.execute('UPDATE tasks SET description = ? WHERE id = ?', (description, task_id))
    if deadline:
        deadline = datetime.strptime(deadline, '%d-%m-%Y').strftime('%Y-%m-%d')
        cursor.execute('UPDATE tasks SET deadline = ? WHERE id = ?', (deadline, task_id))
    if status:
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    if priority:
        cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
    conn.commit()
    conn.close()
    print("Task updated successfully!")

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    if not task:
        print("No task found with the given ID.")
        return
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    print("Task deleted successfully!")

def search_tasks(description):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE description LIKE ?', ('%' + description + '%',))
    rows = cursor.fetchall()
    conn.close()
    tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    return tasks

def sort_tasks(by="deadline"):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    if by == "status":
        tasks.sort(key=lambda task: task.status)
    else:
        tasks.sort(key=lambda task: (task.deadline is None, task.deadline))

    return tasks


def get_due_soon_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE deadline IS NOT NULL')
    rows = cursor.fetchall()
    conn.close()
    tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in rows]
    due_soon_tasks = []
    for task in tasks:
        if task.deadline:
            deadline_date = datetime.strptime(task.deadline, '%Y-%m-%d')
            if deadline_date <= datetime.now() + timedelta(days=1):
                due_soon_tasks.append(task)
    return due_soon_tasks

def display_menu():
    print("\nMain Menu:")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. View pending tasks")
    print("4. View completed tasks")
    print("5. Update a task")
    print("6. Delete a task")
    print("7. Search tasks")
    print("8. Sort tasks")
    print("9. View tasks due soon (within 24 hours)")
    print("10. Exit")

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    for task in tasks:
        deadline_display = datetime.strptime(task.deadline, '%Y-%m-%d').strftime('%d-%m-%Y') if task.deadline else 'None'
        print(f"ID: {task.id}, Description: {task.description}, Deadline: {deadline_display}, Status: {task.status}, Priority: {task.priority}")

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, '%d-%m-%Y')
        current_date = datetime.now().date()
        if date.date() < current_date:
            return False
        year, month, day = date.year, date.month, date.day
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if month in [4, 6, 9, 11] and day > 30:
            return False
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                if day > 29:
                    return False
            elif day > 28:
                return False
        return True
    except ValueError:
        return False

def main():
    create_table()
    due_soon_tasks = get_due_soon_tasks()
    if due_soon_tasks:
        print("--------------------------------------------------------------------------------------")
        print("Reminder: The following tasks are due soon:")
        display_tasks(due_soon_tasks)
        print("--------------------------------------------------------------------------------------")
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (DD-MM-YYYY): ")
            if deadline and not validate_date(deadline):
                print("Invalid date. Please enter a valid date.")
                continue
            if not deadline:
                deadline = '31-12-2999'   #because when None is given for no deadline, while sorting it comes 1st so to avoid it we give verybig deadline 
            status = 'pending'
            priority = input("Enter task priority (high, medium, low): ")
            add_task(description, deadline, status, priority)
            print("Task added successfully!")
        elif choice == '2':
            tasks = get_all_tasks()
            display_tasks(tasks)
        elif choice == '3':
            tasks = get_tasks_by_status('pending')
            display_tasks(tasks)
        elif choice == '4':
            tasks = get_tasks_by_status('completed')
            display_tasks(tasks)
        elif choice == '5':
            task_id = int(input("Enter task ID to update: "))
            description = input("Enter new description (leave blank to skip): ")
            deadline = input("Enter new deadline (DD-MM-YYYY, leave blank to skip): ")
            if deadline and not validate_date(deadline):
                print("Invalid date. Please enter a valid date.")
                continue
            if not deadline:
                deadline = '31-12-2999'
            status = input("Enter new status (leave blank to skip or 'completed'): ")
            priority = input("Enter new priority (leave blank to skip): ")
            update_task(task_id, description or None, deadline or None, status or None, priority or None)
        elif choice == '6':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == '7':
            keyword = input("Enter keyword to search in task descriptions: ")
            tasks = search_tasks(keyword)
            display_tasks(tasks)
        elif choice == '8':
            sort_by = input("Sort by (deadline/status): ").lower()
            tasks = sort_tasks(by=sort_by)
            display_tasks(tasks)
        elif choice == '9':
            tasks = get_due_soon_tasks()
            display_tasks(tasks)
        elif choice == '10':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
