# Task Management Program

This is a simple task management program that allows users to add, update, delete, and view tasks. The program also includes features for sorting tasks by deadline or status, searching tasks by description, and viewing tasks that are due soon.

## How to Run the Program

1. **Prerequisites:**
   - Ensure you have Python 3.x installed on your system.
   - Ensure you have SQLite3 installed (it comes with Python standard library).

2. **Clone the Repository:**
   ```sh
   git clone [<repository-url>](https://github.com/prasanna1221/Task-Management-Application.git)
   cd Task-Management-Application
   ```

Run the Program:
   ```sh
   python Task_management_app.py
   ```

# Features
## Main Menu
The main menu provides the following options:
### -Add a task
-View all tasks
-View pending tasks
-View completed tasks
-Update a task
-Delete a task
-Search tasks
-Sort tasks
-View tasks due soon (within 24 hours)
-Exit
Additional Features
-Date Format: The program uses the DD-MM-YYYY date format for input and display.
-Date Validation: The program validates the entered date to ensure it is a valid date and not in the past.
-Due Date Reminders: The program notifies users about tasks that are due soon (within 24 hours) when the program starts.
-Sorting Tasks: Tasks can be sorted by deadline or status. Tasks with no deadline are considered the least priority and appear at the end of the list.
-Default Deadline: If no deadline is provided while adding or updating a task, a far future date (31-12-2999) is assigned to ensure these tasks appear at the end of the list when sorting by deadline.
Assumptions and Design Decisions
-Date Format: The program assumes that the user will enter dates in the DD-MM-YYYY format.
-Default Deadline: Tasks with no deadline are assigned a far future date (31-12-2999) to ensure they appear at the end of the list when sorting by deadline.
-Date Validation: The program validates the entered date to ensure it is a valid date and not in the past. This includes checking for valid days in a month, leap years, etc.
-Database: The program uses SQLite3 for storing task data. The database file is named tasks.db.
-Task ID Check: The program checks if a task ID exists before attempting to delete or update a task. If the task ID does not exist, a message is displayed to the user.
