from PySide6.QtWidgets import QMessageBox

from src.task_item import TaskItem

class TaskManager():
    """
    Manage all tasks and tasks operations for the Gantt View.
    """

    def __init__(self):
        self._tasks: dict[int, TaskItem] = {}

    def add_task(self, task_json: dict):
        """
        Creates a new TaskItem and adds it to the manager.
        """
        try:
            new_task = TaskItem(task_json)
            self._tasks[new_task.id] = new_task
            return new_task
        except (KeyError, ValueError) as e:
            QMessageBox.warning(
                None,
                "Task Creation Error",
                f"Failed to add task: {e}"
            )

    def get_task(self, task_id: int) -> TaskItem | None:
        """
        Retrieves a task by its ID.
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[TaskItem]:
        """
        Returns a list of all managed Task objects.
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, task_data: dict) -> bool:
        """
        Updates an existing task.
        """
        task = self.get_task(task_id)
        if task:
            try:
                task.update(task_data)
                return True
            except (KeyError, ValueError) as e:
                QMessageBox.warning(
                    None,
                    "Task Update Error",
                    f"Failed to update task: {e}"
                )
                return False
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Deletes a task by its ID.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def load_from_raw_data(self, raw_data: list[dict]):
        """
        Loads tasks from a list of raw dictionaries.
        """
        self._tasks.clear() # Clear existing tasks
        TaskItem._next_id = 0 #Reset ID counter
        for task_dict in raw_data:
            try:
                task = TaskItem(task_dict)
                self._tasks[task.id] = task
            except KeyError as e:
                print(f"Error: Missing key in task data: {e} for task {task_dict}")
            except ValueError as e:
                print(f"Error creating Task object: {e}")
