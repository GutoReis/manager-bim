from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit, QDialog, QDoubleSpinBox, QFormLayout, QHBoxLayout, QLineEdit, QPushButton

from src.task_item import TaskItem

class TaskDialog(QDialog):
    """
    A dialog for creating or editing a task.
    """
    def __init__(self, parent=None, task: TaskItem | None = None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.task = task # Store the task if editing

        self.layout = QFormLayout(self)

        self.name_input = QLineEdit(self)
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.progress_input = QDoubleSpinBox(self)
        self.progress_input.setRange(0.0, 1.0)
        self.progress_input.setSingleStep(0.1)
        self.progress_input.setDecimals(2)

        self.layout.addRow("Task Name:", self.name_input)
        self.layout.addRow("Start Date:", self.start_date_input)
        self.layout.addRow("End Date:", self.end_date_input)
        self.layout.addRow("Progress (0.0 - 1.0:", self.progress_input)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(self.buttons_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Populate fields if editing an existing task
        if self.task:
            self.setWindowTitle(f"Edit Task: {self.task.name}")
            self.name_input.setText(self.task.name)
            self.start_date_input.setDate(self.task.start_date)
            self.end_date_input.setDate(self.task.end_date)
            self.progress_input.setValue(self.task.progress)
        else:
            self.setWindowTitle("Create New Task")
            self.start_date_input.setDate(QDate.currentDate())
            self.end_date_input.setDate(QDate.currentDate().addDays(7))

    def get_task_data(self) -> dict:
        """
        Returns the data entered in the dialog
        """
        return {
            'name': self.name_input.text(),
            'start': self.start_date_input.date().toString("yyyy-MM-dd"),
            'end': self.end_date_input.date().toString("yyyy-MM-dd"),
            'progress': self.progress_input.value(),
            'depends_on': None,
            'group': None
        }
