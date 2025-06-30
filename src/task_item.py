from uuid import uuid4

from PySide6.QtCore import QDate

class TaskItem():
    """
    Manage the Task itens for the Gantt chart.
    """
    def __init__(self, json_data):
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
        self.id = json_data.get('id', str(uuid4()))
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