from PySide6.QtCore import QDate

class TaskItem():
    """
    Represents a singel task in the Gantt Chart.
    Encapsutes task data and provides convenient access.
    """
    # A simple static counter for unique IDs
    _next_id = 0

    def __init__(self, json_data: dict):
        """
        Receives json data with the structure of tasks
        {
            'id': '23123123-12312-321-32132',
            'name': 'Task A',
            'start': '2023-01-01',
            'end': '2023-01-10',
            'progress': 0.7,
            'depends_on': none,
            'group': 'foundation'
        }
        """
        if "id" not in json_data and json_data["id"]:
            self.id = json_data["id"]
            # Ensure _next_id is always greater than any assigned ID
            TaskItem._next_id = max(TaskItem._next_id, self.id + 1)
        else:
            self.id = TaskItem._next_id
            TaskItem._next_id += 1

        self.name = json_data.get('name', None)
        start_date_str = json_data.get('start', None)
        end_date_str = json_data.get('end', None)
        self.progress = json_data.get('progress', 0.0)
        self.depends_on = json_data.get('depends_on', None)
        self.group = json_data.get('group', None)

        if start_date_str:
            self.start_date = QDate.fromString(start_date_str, 'yyyy-MM-dd')

        if end_date_str:
            self.end_date = QDate.fromString(end_date_str, 'yyyy-MM-dd')

        if not self.start_date.isValid():
            raise ValueError(f"Invalid start date format for task '{self.name}': '{start_date_str}'")
        if not self.end_date.isValid():
            raise ValueError(f"Invalid end date format for task '{self.name}': '{end_date_str}'")
        if self.start_date > self.end_date:
            raise ValueError(f"Start date after end date for task '{self.name}'.")
        if self.progress > 1.0 or self.progress < 0.0:
            raise ValueError(f"Progression not between 0.0 and 1.0 for task '{self.name}'")

    def get_duration_days(self) -> int:
        """Calculates the duration of the task in days.
        Adds one to final result to include the end date.

        Returns:
            int: Number of days between start and end
        """
        return self.start_date.daysTo(self.end_date) + 1

    def to_dict(self) -> dict:
        """
        Converts the TaskItem object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'start': self.start_date.toString("yyyy-MM-dd"),
            'end': self.end_date.toString("yyyy-MM-dd"),
            'progress': self.progress,
            'depends_on': self.depends_on,
            'group': self.group
        }
