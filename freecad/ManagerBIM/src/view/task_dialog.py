from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QComboBox, QDateEdit, QDialog, QDoubleSpinBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider

from ..model.task_item import TaskItem

class TaskDialog(QDialog):
    """
    A dialog for creating or editing a task.
    """
    def __init__(self, current_tasks_list: list, parent=None, task: TaskItem | None = None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.task = task # Store the task if editing
        self.actual_progress_value = 0

        self.layout = QFormLayout(self)

        self.name_input = QLineEdit(self)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)

        self.progress_slider_input = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider_input.setMinimum(0)
        self.progress_slider_input.setMaximum(100)
        self.progress_slider_input.setSingleStep(1)
        self.progress_slider_input.sliderMoved.connect(self.slider_value_changed)
        self.progress_value_label = QLabel(
            f"Progress: ({self.progress_slider_input.value()}%)"
        )

        self.depends_on_input = QComboBox(self)
        self.depends_on_input.addItem("None")
        self.depends_on_input.addItems(current_tasks_list)

        self.layout.addRow("Task Name:", self.name_input)
        self.layout.addRow("Start Date:", self.start_date_input)
        self.layout.addRow("End Date:", self.end_date_input)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress_value_label)
        self.progress_layout.addWidget(self.progress_slider_input)
        self.layout.addRow(self.progress_layout)

        self.layout.addRow("Depends on:", self.depends_on_input)

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
            self.progress_slider_input.setValue(self.task.progress * 100)
            if self.task.depends_on:
                self.depends_on_input.setCurrentText(self.task.depends_on)
        else:
            self.setWindowTitle("Create New Task")
            self.start_date_input.setDate(QDate.currentDate())
            self.end_date_input.setDate(QDate.currentDate().addDays(7))

    def slider_value_changed(self, value):
        #self.actual_progress_value = value
        self.progress_value_label.setText(
            f"Progress: ({self.progress_slider_input.value()}%)"
        )

    def get_task_data(self) -> dict:
        """
        Returns the data entered in the dialog
        """
        if self.depends_on_input.currentText() == "None":
            depends_on = None
        else:
            depends_on = self.depends_on_input.currentText()
        return {
            'name': self.name_input.text(),
            'start': self.start_date_input.date().toString("yyyy-MM-dd"),
            'end': self.end_date_input.date().toString("yyyy-MM-dd"),
            'progress': (self.progress_slider_input.value())/100,
            'depends_on': depends_on,
            'group': None
        }
