import json
from json.decoder import JSONDecodeError

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QDialog, QFileDialog,
                               QMessageBox, QToolBar)

from src.task_dialog import TaskDialog


class Toolbar():
    """
    Class for the toolbar to the main window.
    """
    def __init__(self, main_window):
        self.filename = "" # Filename to simplify save action (quick save option)
        self.main_window = main_window
        self.toolbar = QToolBar("Main")
        self.toolbar.setIconSize(QSize(22, 22))

        new_project_action = QAction(
            QIcon("src/assets/new_project.svg"),
            "New Project",
            self.main_window
        )
        new_project_action.setStatusTip("New Project")
        new_project_action.triggered.connect(self.new_project)
        self.toolbar.addAction(new_project_action)

        open_file_action = QAction(
            QIcon("src/assets/open_file.svg"),
            "Open File",
            self.main_window
        )
        open_file_action.setStatusTip("Open File")
        open_file_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_file_action)

        save_file_action = QAction(
            QIcon("src/assets/save_file.svg"),
            "Save file",
            self.main_window
        )
        save_file_action.setStatusTip("Save File")
        save_file_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_file_action)

        save_new_action = QAction(
            QIcon("src/assets/save_new.svg"),
            "Save as new",
            self.main_window
        )
        save_new_action.setStatusTip("Save as new")
        save_new_action.triggered.connect(self.save_as_new_file)
        self.toolbar.addAction(save_new_action)

        add_task_action = QAction(
            QIcon("src/assets/add_task.svg"),
            "Add task",
            self.main_window
        )
        add_task_action.setStatusTip("Add new task")
        add_task_action.triggered.connect(self.add_task)
        self.toolbar.addAction(add_task_action)

        edit_task_action = QAction(
            QIcon("src/assets/edit_task.svg"),
            "Edit task",
            self.main_window
        )
        edit_task_action.setStatusTip("Edit task")
        edit_task_action.triggered.connect(self.edit_task)
        self.toolbar.addAction(edit_task_action)

        delete_task_action = QAction(
            QIcon("src/assets/delete_task.svg"),
            "Delete task",
            self.main_window
        )
        delete_task_action.setStatusTip("Delete task")
        delete_task_action.triggered.connect(self.delete_task)
        self.toolbar.addAction(delete_task_action)

        play_sim_action = QAction(
            QIcon("src/assets/start_sim.svg"),
            "Play Sim",
            self.main_window
        )
        play_sim_action.setStatusTip("Play simulation")
        play_sim_action.triggered.connect(self.main_window.simulation_manager.start_simulation)
        self.toolbar.addAction(play_sim_action)

        stop_sim_action = QAction(
            QIcon("src/assets/stop_sim.svg"),
            "Stop Sim",
            self.main_window
        )
        stop_sim_action.setStatusTip("Stop simulation")
        stop_sim_action.triggered.connect(self.main_window.simulation_manager.stop_simulation)
        self.toolbar.addAction(stop_sim_action)

    def new_project(self):
        """
        Clear the scene and start new project.
        """
        if not self.main_window.task_manager.get_all_tasks():
            return
        reply = QMessageBox.question(
            self.main_window,
            "New Project",
            f"Are you sure you want to start a new project?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No:
            return
        self.main_window.task_manager.remove_all_tasks()
        self.main_window.gantt_chart_widget.start_date = None
        self.main_window.gantt_chart_widget.end_date = None
        self.main_window.refresh_gantt_chart()


    def open_file(self):
        """
        Load a JSON file from system to load the Gantt Chart.
        """
        file_data = list()
        self.filename, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Select file",
            "/",
            "Json Files (*.json)"
        )

        try:
            if self.filename:
                with open(self.filename, "r") as source_file:
                    file_data = json.load(source_file)
            self.main_window.task_manager.load_from_raw_data(file_data["tasks"])
            self.main_window.refresh_gantt_chart()
        except JSONDecodeError:
            QMessageBox.critical(
                self.main_window,
                "File has no data",
                f"Erro loading the file {self.filename}. File has no data."
            )
            return
        except KeyError:
            QMessageBox.critical(
                self.main_window,
                "File has no tasks",
                f'Erro loading the file {self.filename}. JSON File has no "tasks" key.'
            )
            return

    def save_file(self):
        """
        Save the plan as a JSON file.

        If the chart is created as new, no file was opened, then it triggers the save as new.
        If the chart was opened from a file, or already saved, then it uses the value path from filename.
        """
        if not self.filename:
            self.save_as_new_file()
            return

        file_data = self.main_window.task_manager.export_as_raw_data()
        with open(self.filename, "w") as file_output:
            file_output.write(json.dumps(file_data, indent=4))

    def save_as_new_file(self):
        """
        Start a dialog to select the path and define the name of the file to save.

        If file already exists, it appears a dialog to confirm the overwrite.
        """
        temp_filename, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Save as new",
            ".",
            "Json Files (*.json)"
        )

        if temp_filename:
            file_data = self.main_window.task_manager.export_as_raw_data()
            with open(temp_filename, "w") as file_output:
                file_output.write(json.dumps(file_data, indent=4))
            self.filename = temp_filename

    def add_task(self):
        """
        Opens a dialog to add a new task.
        """
        dialog = TaskDialog(
            current_tasks_list=self.main_window.task_manager.get_all_tasks_str(),
            parent=self.main_window
        )
        if dialog.exec() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            new_task = self.main_window.task_manager.add_task(task_data)
            if new_task:
                self.main_window.refresh_gantt_chart()
                QMessageBox.information(
                    self.main_window,
                    "Task Added",
                    f"Task '{new_task.name}' added successfully."
                )

    def edit_task(self):
        """
        Opens a dialog to edit the selected task.
        """
        selected_task_id = getattr(
            self.main_window.gantt_chart_widget,
            'selected_task_id',
            None
        )
        if selected_task_id is None:
            QMessageBox.warning(
                self.main_window,
                "No Task Selected",
                "Please selecta a task on the chart to edit"
            )
            return

        task_to_edit = self.main_window.task_manager.get_task(selected_task_id)
        if not task_to_edit:
            QMessageBox.critical(
                self.main_window,
                "Task Not Found",
                f"Task with ID {selected_task_id} not found."
            )
            return

        #dialog = TaskDialog(self, task=task_to_edit)
        dialog = TaskDialog(
            current_tasks_list=self.main_window.task_manager.get_all_tasks_str(),
            parent=self.main_window,
            task=task_to_edit
        )
        if dialog.exec() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            edited = self.main_window.task_manager.update_task(
                selected_task_id,
                task_data
            )
            if edited:
                self.main_window.refresh_gantt_chart()
                QMessageBox.information(
                    self.main_window,
                    "Taks Updated",
                    f"Task '{task_data['name']}' updated succesfully."
                )

    def delete_task(self):
        """
        Deletes the selected task.
        """
        selected_task_id = getattr(
            self.main_window.gantt_chart_widget,
            'selected_task_id',
            None
        )
        if selected_task_id is None:
            QMessageBox.warning(
                self.main_window,
                "No Task Selected",
                "Please select a task on the chart to delete"
            )
            return

        task_to_delete = self.main_window.task_manager.get_task(selected_task_id)
        if not task_to_delete:
            QMessageBox.critical(
                self.main_window,
                "Task Not Found",
                f"Task with ID {selected_task_id} not found."
            )
            return

        # Confirmation dialog
        reply = QMessageBox.question(
            self.main_window,
            "Delete Task",
            f"Are you sure you want to delete task '{task_to_delete.name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            deleted = self.main_window.task_manager.delete_task(selected_task_id)
            if deleted:
                self.main_window.refresh_gantt_chart()
                QMessageBox.information(
                    self.main_window,
                    "Task Deleted",
                    f"Task '{task_to_delete.name}' deleted suffessfully."
                )
            else:
                QMessageBox.critical(
                    self.main_window,
                    "Deletion Failed",
                    f"Failed to delete task '{task_to_delete.name}'."
                )
