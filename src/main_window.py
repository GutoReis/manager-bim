from PySide6.QtWidgets import QDialog, QHBoxLayout, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from src.gantt_chart_widget import GanttChartWidget
from src.task_manager import TaskManager
from src.task_dialog import TaskDialog

class MainWindow(QMainWindow):
    """
    Main window for the Gantt chart application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ManagerBIM')
        self.setGeometry(100, 100, 1000, 600) # x,y,width,height

        self.task_manager = TaskManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Buttons for task management
        button_layout = QHBoxLayout()
        self.add_task_button = QPushButton("Add Task")
        self.edit_task_button = QPushButton("Edit Task")
        self.delete_task_button = QPushButton("Delete Task")

        button_layout.addWidget(self.add_task_button)
        button_layout.addWidget(self.edit_task_button)
        button_layout.addWidget(self.delete_task_button)
        layout.addLayout(button_layout)

        self.gantt_chart_widget = GanttChartWidget(self)
        layout.addWidget(self.gantt_chart_widget)

        # Connect buttons to methods
        self.add_task_button.clicked.connect(self.add_task)
        self.edit_task_button.clicked.connect(self.edit_task)
        self.delete_task_button.clicked.connect(self.delete_task)

        # TODO: Change to load from file (using button)
        self.load_sample_data()
        self.refresh_gantt_chart()

    def load_sample_data(self):
        """
        Loads some sample task data into the Gantt Chart.
        """
        sample_tasks = [
            {'name': 'Project Planning', 'start': '2025-01-01', 'end': '2025-01-15', 'progress': 0.9, 'id': 1001},
            {'name': 'Requirements Gathering', 'start': '2025-01-10', 'end': '2025-01-25', 'progress': 0.7, 'id': 1002},
            {'name': 'Design Phase', 'start': '2025-01-20', 'end': '2025-02-10', 'progress': 0.5, 'id': 1003},
            {'name': 'Development - Module A', 'start': '2025-02-01', 'end': '2025-02-28', 'progress': 0.3, 'id': 1004},
            {'name': 'Development - Module B', 'start': '2025-02-15', 'end': '2025-03-10', 'progress': 0.0, 'id': 1005},
            {'name': 'Testing', 'start': '2025-03-01', 'end': '2025-03-20', 'progress': 0.0, 'id': 1006},
            {'name': 'Deployment', 'start': '2025-03-25', 'end': '2025-03-30', 'progress': 0.0, 'id': 1007},
        ]
        # self.gantt_chart_widget.set_tasks(sample_tasks)
        self.task_manager.load_from_raw_data(sample_tasks)

    def refresh_gantt_chart(self):
        """
        Refreshes the Gantt chart with the latest data from TaskManager.
        """
        self.gantt_chart_widget.set_tasks(self.task_manager.get_all_tasks())

    def add_task(self):
        """
        Opens a dialog to add a new task.
        """
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            new_task = self.task_manager.add_task(task_data)
            if new_task:
                self.refresh_gantt_chart()
                QMessageBox.information(
                    self,
                    "Task Added",
                    f"Task '{new_task.name}' added successfully."
                )

    def edit_task(self):
        """
        Opens a dialog to edit the selected task.
        """
        selected_task_id = getattr(self.gantt_chart_widget, 'selected_task_id', None)
        if selected_task_id is None:
            QMessageBox.warning(
                self,
                "No Task Selected",
                "Please selecta a task on the chart to edit"
            )
            return

        task_to_edit = self.task_manager.get_task(selected_task_id)
        if not task_to_edit:
            QMessageBox.critical(
                self,
                "Task Not Found",
                f"Task with ID {selected_task_id} not found."
            )
            return

        dialog = TaskDialog(self, task=task_to_edit)
        if dialog.exec() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            edited = self.task_manager.update_task(selected_task_id, task_data)
            if edited:
                self.refresh_gantt_chart()
                QMessageBox.information(
                    self,
                    "Taks Updated",
                    f"Task '{task_data['name']}' updated succesfully."
                )

    def delete_task(self):
        """
        Deletes the selected task.
        """
        selected_task_id = getattr(self.gantt_chart_widget, 'selected_task_id', None)
        if selected_task_id is None:
            QMessageBox.warning(
                self,
                "No Task Selected",
                "Please select a task on the chart to delete"
            )
            return

        task_to_delete = self.task_manager.get_task(selected_task_id)
        if not task_to_delete:
            QMessageBox.critical(
                self,
                "Task Not Found",
                f"Task with ID {selected_task_id} not found."
            )
            return

        # Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Are you sure you want to delete task '{task_to_delete.name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            deleted = self.task_manager.delete_task(selected_task_id)
            if deleted:
                self.refresh_gantt_chart()
                QMessageBox.information(
                    self,
                    "Task Deleted",
                    f"Task '{task_to_delete.name}' deleted suffessfully."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Deletion Failed",
                    f"Failed to delete task '{task_to_delete.name}'."
                )
