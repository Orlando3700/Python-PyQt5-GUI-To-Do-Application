# Provides access to system-specific parameters and
# functions (like sys.argv for app startup).
import sys
import json

# from PyQt5.QtWidgets import ...: Imports essential PyQt5
# widgets used to build the GUI:
# QApplication: Manages the application’s control flow and main settings.
# QWidget: The base class for all UI objects.
# QVBoxLayout, QHBoxLayout: Layout managers to arrange
# widgets vertically/horizontally.
# QLineEdit: A single-line text input field.
# QPushButton: A clickable button.
# QListWidget: A widget to show a list of items.
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QDialog, QLabel

from PyQt5.QtGui import QFont, QBrush, QColor
from test.test_decimal import file

# This defines a new class EditDialog that inherits from
# QDialog, which is a built-in PyQt5 class used to create
# popup windows (dialogs).
class EditDialog(QDialog):
    # This is the constructor method that runs when a new EditDialog is created.
    # old_text is the current task text that will be edited.
    def __init__(self, old_text):
        # Calls the constructor of the parent class
        # (QDialog) to ensure the dialog is properly initialized.
        super().__init__()
        # Sets the title of the dialog window 
        self.setWindowTitle("Edit Task")
        self.setGeometry(150, 150, 300, 100)
        # Creates a vertical layout so widgets stack from top to bottom.
        self.layout = QVBoxLayout()

        # Creates a single-line text input field where the user can edit the task
        self.input_field = QLineEdit()
        # Pre-fills the text field with the current task text, so the user can edit it.
        self.input_field.setText(old_text)
        # Creates a button labeled "Save" which will be clicked to confirm the changes.
        self.save_button = QPushButton("Save")

        # Adds a label above the input field that says "Edit task:"
        self.layout.addWidget(QLabel("Edit task:"))
        # Adds the text field and save button to the layout, one below the other.
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.save_button)

        # Applies the vertical layout to the dialog so everything appears correctly.
        self.setLayout(self.layout)

        # Connects the Save button to the accept() method
        # accept() closes the dialog and tells the parent that the user confirmed the input.
        self.save_button.clicked.connect(self.accept)
    
    # Defines a custom method that:
    # Retrieves the text from the input field.
    # Strips extra spaces from the beginning and end.
    # Returns the cleaned-up string to be used as the new task.
    def get_updated_text(self):
        return self.input_field.text().strip()

# Defines a custom class ToDoApp, which inherits from QWidget, making it a GUI window.
class ToDoApp(QWidget):
    # __init__: The constructor method that sets up the GUI when an object is created.
    def __init__(self):
        # Calls the parent class (QWidget) constructor to properly initialize the window.
        super().__init__()
        # Sets the window title and size/position
        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 400, 350)
        
        # A Python list to keep track of tasks internally
        # self.tasks = []
        
        # Creates a vertical layout manager to stack widgets vertically.
        self.layout = QVBoxLayout()
        
        self.tasks = {}
        
        # Inpuit field and add button layout
        input_layout = QHBoxLayout()
        # A text input field for entering new tasks.
        self.input_field = QLineEdit()
        # A button labeled "Add Task" to trigger adding tasks.
        self.add_button = QPushButton("Add Task")
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        
        # A widget that displays all added tasks as a list.
        self.task_list = QListWidget()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Delete button
        self.delete_button = QPushButton("Delete Selected Task")
        # Edit button       
        self.edit_button = QPushButton("Edit Selected Task")
        # Add delete button to layout
        button_layout.addWidget(self.delete_button)
        # Add edit button to layout
        button_layout.addWidget(self.edit_button)
        
        # Adds the widgets to the vertical layout (top-to-bottom order).
        # self.layout.addWidget(self.input_field)
        # self.layout.addWidget(self.add_button)
        
        # Add widgets to main layout
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.task_list)
        self.layout.addLayout(button_layout)
        
        # self.layout.addWidget(self.delete_button)
        
        # Applies the vertical layout to the window,
        # finalizing the UI structure.
        self.setLayout(self.layout)
        
        # Connects the button’s click event to the add_task
        # method — so when clicked, it triggers that function.
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task);
        self.edit_button.clicked.connect(self.edit_task)
        self.task_list.itemClicked.connect(self.toggle_task_status)
        
        self.setStyleSheet("background-color: #f0f0f0;")  # Background color

        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid gray;
                border-radius: 4px;
                background-color: white;
            }
        """)

        # Green for Add
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Red for Delete
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
        QPushButton:hover {
            background-color: #d32f2f;
        }
    """)

        # Yellow for Edit
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                font-weight: bold;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
        QPushButton:hover {
            background-color: #e6ac00;
        }
    """)

        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        
        # Load existing tasks
        self.load_tasks()
        
    # This defines a method to save all current tasks to a file.    
    def save_tasks(self, filename="tasks.json"):
        # Opens the file named tasks.json in write mode ("w").
        # with ensures the file is properly closed after writing.
        with open(filename, "w") as file:
            # Saves (dumps) the self.tasks dictionary to the file in JSON format.
            # This records both the task names and their completion status
            json.dump(self.tasks, file)
    
    # This method attempts to load tasks from a file.        
    def load_tasks(self, filename="tasks.json"):
        # Attempts to open the file in read mode ("r")
        try:
            with open(filename, "r") as file:
                # Loads the JSON content and stores it in self.tasks
                self.tasks = json.load(file)
                # Loops through each saved task and its completion status.
                # Calls add_list_item() to recreate the visual list in the GUI.
                for task, completed in self.tasks.items():
                    self.add_list_item(task, completed)
        except FileNotFoundError:
            self.tasks = {}
    
    # Gets the text from the input field.
    def add_task(self):
        # Gets the text entered by the user in the input field.
        task = self.input_field.text()
        # The input is not empty.
        # The task doesn't already exist in the internal self.tasks dictionary.
        if task and task not in self.tasks:
            # Adds the new task to the internal dictionary.
            self.tasks[task] = False  # Not completed
            # Adds the task visually to the list widget using a helper method.
            self.add_list_item(task, False)
            # Clears the input field for the next entry.
            self.input_field.clear()
            self.save_tasks() # Save after adding

        # if task:    # Checks if the input is not empty.
            # self.tasks.append(task) # Adds the task to the internal list.
            # self.task_list.addItem(task) # Displays the task in the GUI list.
    
    def delete_task(self):
        # Gets a list of all selected (highlighted) items in the list.
        selected_items = self.task_list.selectedItems()
        # Loops through all selected tasks
        for item in selected_items:
            # Removes the checkmark symbol if present to get the actual task text.
            task_text = item.text().replace("✔ ", "")  # Strip checkmark
            if task_text in self.tasks:
                # Removes the task from the internal dictionary
                del self.tasks[task_text]
                # Remove from UI list
                self.task_list.takeItem(self.task_list.row(item))
                self.save_tasks() # Save after deleting
            
            # Remove from internal list
            # self.tasks.remove(item.text())
    
    def toggle_task_status(self, item):
        # Strips the checkmark from the displayed task name to get the real key.
        task_text = item.text().replace("✔ ", "")
        if task_text in self.tasks:
            # Reverses the current completion status (True becomes False and vice versa).
            self.tasks[task_text] = not self.tasks[task_text]  # Toggle status
            # Updates the visual appearance of the task to reflect the new status
            self.update_list_item(item, task_text, self.tasks[task_text])
            self.save_tasks() # Save after status change
        
    def edit_task(self):
        # Gets the selected task. If none is selected, it exits the function.
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return
        # Retrieves the original text (stripping the checkmark) and the task’s completion status.
        item = selected_items[0]
        old_text = item.text().replace("✔ ", "")
        completed = self.tasks[old_text]

        # Creates a pop-up dialog with the current task text already filled in.
        dialog = EditDialog(old_text)
        # Opens the dialog and waits for the user to click "Save". Returns True if they do.
        if dialog.exec_():
            # Retrieves the edited task name from the dialog.
            new_text = dialog.get_updated_text()
            # Validates the new text: it's not empty, not the same as the original, and not a duplicate.
            if new_text and new_text != old_text and new_text not in self.tasks:
                # Updates the internal dictionary: removes the old entry and adds the new one.
                del self.tasks[old_text]
                self.tasks[new_text] = completed
                item.setText("")  # Clear current item temporarily
                # Updates the visible list item with the new task name and status
                self.update_list_item(item, new_text, completed)
                self.save_tasks() # Save after editing

    def add_list_item(self, task, completed):
        # Creates a new list widget item.
        item = QListWidgetItem()
        # Sets the text, font, and color for the item using another helper.
        self.update_list_item(item, task, completed)
        # Adds the item to the GUI list so the user sees it.
        self.task_list.addItem(item)

    def update_list_item(self, item, task, completed):
        # Adds a checkmark in front of the task name if it's completed.
        prefix = "✔ " if completed else ""
        # Sets the full display text for the task item.
        item.setText(prefix + task)
        # Applies a strike-through font if the task is completed.
        font = QFont()
        font.setStrikeOut(completed)
        item.setFont(font)
        # Sets the text color: gray for completed tasks, black for active ones.
        item.setForeground(QBrush(QColor("gray") if completed else QColor("black")))

# This block runs the app only if this file is executed directly.
if __name__ == "__main__":
    # Creates the application instance and passes command-line arguments.
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-family: Arial; font-size: 14px; }")
    # Creates the main app window and displays it.
    window = ToDoApp()
    window.show()
    # Starts the application’s event loop (waiting for user interaction).
    # sys.exit ensures the program exits cleanly when the window is closed.
    sys.exit(app.exec_())
    
    
    