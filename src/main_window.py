import json
from json.decoder import JSONDecodeError

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QDialog, QFileDialog, QHBoxLayout,
                               QMainWindow, QMessageBox, QPushButton, QToolBar,
                               QVBoxLayout, QWidget)

from src.gantt_chart_widget import GanttChartWidget
from src.simulation_manager import SimulationManager
#from src.task_dialog import TaskDialog
from src.task_manager import TaskManager
from src.toolbar import Toolbar

class MainWindow(QMainWindow):
    """
    Main window for the Gantt chart application.
    """
    def __init__(self):
        super().__init__()
        #self.filename = "" # Filename to simplify save action (quick save option)
        self.setWindowTitle('ManagerBIM')
        self.setGeometry(100, 100, 1000, 600) # x,y,width,height

        self.task_manager = TaskManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.gantt_chart_widget = GanttChartWidget(parent=self, task_manager=self.task_manager)
        layout.addWidget(self.gantt_chart_widget)

        self.simulation_manager = SimulationManager(self.gantt_chart_widget, self.task_manager)

        # Buttons for task management
        # # TODO Change this buttons to Toolbar style and place on different file
        #button_layout = QHBoxLayout()
        #self.open_file_button = QPushButton("Open File")
        #self.save_file_button = QPushButton("Save File")
        #self.save_new_file_button = QPushButton("Save As")
        #self.add_task_button = QPushButton("Add Task")
        #self.edit_task_button = QPushButton("Edit Task")
        #self.delete_task_button = QPushButton("Delete Task")
        #self.play_button = QPushButton("Play Simulation")
        #self.stop_button = QPushButton("Stop Simulation")

        #toolbar = QToolBar("Main")
        #toolbar.setIconSize(QSize(16, 16))
        toolbar = Toolbar(main_window=self)
        self.addToolBar(toolbar.toolbar)


        # open_file_action = QAction(
        #     QIcon("src/assets/open_file.png"),
        #     "Open File",
        #     self
        # )
        #open_file_action.setStatusTip("Open File")
        #open_file_action.triggered.connect(self.open_file)
        #open_file_action.setCheckable(True)
        #toolbar.addAction(open_file_action)

        #self.addToolBar(toolbar)

        #button_layout.addWidget(self.open_file_button)
        #button_layout.addWidget(self.save_file_button)
        #button_layout.addWidget(self.save_new_file_button)
        #button_layout.addWidget(self.add_task_button)
        #button_layout.addWidget(self.edit_task_button)
        #button_layout.addWidget(self.delete_task_button)
        #button_layout.addWidget(self.play_button)
        #button_layout.addWidget(self.stop_button)
        #layout.addLayout(button_layout)



        # Connect buttons to methods
        #self.open_file_button.clicked.connect(self.open_file)
        #self.save_file_button.clicked.connect(self.save_file)
        #self.save_new_file_button.clicked.connect(self.save_as_new_file)
        #self.add_task_button.clicked.connect(self.add_task)
        #self.edit_task_button.clicked.connect(self.edit_task)
        #self.delete_task_button.clicked.connect(self.delete_task)
        #self.play_button.clicked.connect(self.simulation_manager.start_simulation)
        #self.stop_button.clicked.connect(self.simulation_manager.stop_simulation)

        self.refresh_gantt_chart()

    # def load_sample_data(self):
    #     """
    #     Loads some sample task data into the Gantt Chart.
    #     """
    #     sample_tasks = [
    #         {'name': 'Project Planning', 'start': '2025-01-01', 'end': '2025-01-15', 'progress': 0.9, 'id': 1001},
    #         {'name': 'Requirements Gathering', 'start': '2025-01-10', 'end': '2025-01-25', 'progress': 0.7, 'id': 1002},
    #         {'name': 'Design Phase', 'start': '2025-01-20', 'end': '2025-02-10', 'progress': 0.5, 'id': 1003},
    #         {'name': 'Development - Module A', 'start': '2025-02-01', 'end': '2025-02-28', 'progress': 0.3, 'id': 1004},
    #         {'name': 'Development - Module B', 'start': '2025-02-15', 'end': '2025-03-10', 'progress': 0.0, 'id': 1005},
    #         {'name': 'Testing', 'start': '2025-03-01', 'end': '2025-03-20', 'progress': 0.0, 'id': 1006},
    #         {'name': 'Deployment', 'start': '2025-03-25', 'end': '2025-03-30', 'progress': 0.0, 'id': 1007},
    #     ]
    #     # self.gantt_chart_widget.set_tasks(sample_tasks)
    #     self.task_manager.load_from_raw_data(sample_tasks)

    #def open_file(self):
    #    """
    #    Load a JSON file from system to load the Gantt Chart.
    #    """
    #    file_data = list()
    #    self.filename, _ = QFileDialog.getOpenFileName(
    #        self,
    #        "Select file",
    #        "/",
    #        "Json Files (*.json)"
    #    )
    #    try:
    #        if self.filename:
        #            with open(self.filename, "r") as source_file:
            #                file_data = json.load(source_file)
            #        # return file_data["tasks"]
            #        self.task_manager.load_from_raw_data(file_data["tasks"])
            #        self.refresh_gantt_chart()
            #    except JSONDecodeError:
                #        QMessageBox.critical(
                #            self,
                #            "File has no data",
                #            f"Erro loading the file {self.filename}. File has no data."
                #        )
                #        return
                #    except KeyError:
                    #        QMessageBox.critical(
                    #            self,
                    #            "File has no tasks",
                    #            f'Erro loading the file {self.filename}. JSON File has no "tasks" key.'
                    #        )
                    #        return

    #def save_file(self):
    #    """
    #    Save the plan as a JSON file.
    #
    #    If the chart is created as new, no file was opened, then it triggers the save as new.
    #    If the chart was opened from a file, or already saved, then it uses the value path from filename.
    #    """
    #    if not self.filename:
        #        self.save_as_new_file()
        #        return
        #
        #    file_data = self.task_manager.export_as_raw_data()
    #    with open(self.filename, "w") as file_output:
        #        file_output.write(json.dumps(file_data, indent=4))
        #
    #def save_as_new_file(self):
        #    """
        #    Start a dialog to select the path and define the name of the file to save.
        #
        #    If file already exists, it appears a dialog to confirm the overwrite.
    #    """
    #    temp_filename, _ = QFileDialog.getSaveFileName(
    #        self,
    #        "Save as new",
    #        ".",
    #        "Json Files (*.json)"
    #    )
    #
    #    if temp_filename:
        #        file_data = self.task_manager.export_as_raw_data()
        #        with open(temp_filename, "w") as file_output:
            #            file_output.write(json.dumps(file_data, indent=4))
            #        self.filename = temp_filename

    def refresh_gantt_chart(self):
        """
        Refreshes the Gantt chart with the latest data from TaskManager.
        """
        self.gantt_chart_widget.set_tasks(self.task_manager.get_all_tasks())

    #def add_task(self):
    #    """
    #    Opens a dialog to add a new task.
    #    """
    #    dialog = TaskDialog(
    #        current_tasks_list=self.task_manager.get_all_tasks_str(),
    #        parent=self
    #    )
    #    if dialog.exec() == QDialog.Accepted:
        #        task_data = dialog.get_task_data()
        #        new_task = self.task_manager.add_task(task_data)
        #        if new_task:
            #            self.refresh_gantt_chart()
            #            QMessageBox.information(
            #                self,
            #                "Task Added",
            #                f"Task '{new_task.name}' added successfully."
            #            )

    #def edit_task(self):
    #    """
    #    Opens a dialog to edit the selected task.
    #    """
    #    selected_task_id = getattr(self.gantt_chart_widget, 'selected_task_id', None)
    #    if selected_task_id is None:
        #        QMessageBox.warning(
        #            self,
        #            "No Task Selected",
        #            "Please selecta a task on the chart to edit"
        #        )
        #        return
        #
        #    task_to_edit = self.task_manager.get_task(selected_task_id)
    #    if not task_to_edit:
        #        QMessageBox.critical(
        #            self,
        #            "Task Not Found",
        #            f"Task with ID {selected_task_id} not found."
        #        )
        #        return
        #
        #    #dialog = TaskDialog(self, task=task_to_edit)
    #    dialog = TaskDialog(
    #        current_tasks_list=self.task_manager.get_all_tasks_str(),
    #        parent=self,
    #        task=task_to_edit
    #    )
    #    if dialog.exec() == QDialog.Accepted:
        #        task_data = dialog.get_task_data()
        #        edited = self.task_manager.update_task(selected_task_id, task_data)
        #        if edited:
            #            self.refresh_gantt_chart()
            #            QMessageBox.information(
            #                self,
            #                "Taks Updated",
            #                f"Task '{task_data['name']}' updated succesfully."
            #            )

    #def delete_task(self):
    #    """
    #    Deletes the selected task.
    #    """
    #    selected_task_id = getattr(self.gantt_chart_widget, 'selected_task_id', None)
    #    if selected_task_id is None:
        #        QMessageBox.warning(
        #            self,
        #            "No Task Selected",
        #            "Please select a task on the chart to delete"
        #        )
        #        return
        #
        #    task_to_delete = self.task_manager.get_task(selected_task_id)
    #    if not task_to_delete:
        #        QMessageBox.critical(
        #            self,
        #            "Task Not Found",
        #            f"Task with ID {selected_task_id} not found."
        #        )
        #        return
        #
        #    # Confirmation dialog
    #    reply = QMessageBox.question(
    #        self,
    #        "Delete Task",
    #        f"Are you sure you want to delete task '{task_to_delete.name}'?",
    #        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    #    )
    #    if reply == QMessageBox.Yes:
        #        deleted = self.task_manager.delete_task(selected_task_id)
        #        if deleted:
            #            self.refresh_gantt_chart()
            #            QMessageBox.information(
            #                self,
            #                "Task Deleted",
            #                f"Task '{task_to_delete.name}' deleted suffessfully."
            #            )
    #        else:
        #            QMessageBox.critical(
        #                self,
        #                "Deletion Failed",
        #                f"Failed to delete task '{task_to_delete.name}'."
        #            )
