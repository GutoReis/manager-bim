from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from src.gantt_chart_widget import GanttChartWidget

class MainWindow(QMainWindow):
    """
    Main window for the Gantt chart application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ManagerBIM')
        self.setGeometry(100, 100, 1000, 600) # x,y,width,height

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.gantt_chart_widget = GanttChartWidget(self)
        layout.addWidget(self.gantt_chart_widget)

        # TODO: Change to load from file (using button)
        self.load_sample_data()

    def load_sample_data(self):
        """
        Loads some sample task data into the Gantt Chart.
        """
        sample_tasks = [
            {'name': 'Project Planning', 'start': '2023-01-01', 'end': '2023-01-15', 'progress': 0.9},
            {'name': 'Requirements Gathering', 'start': '2023-01-10', 'end': '2023-01-25', 'progress': 0.7},
            {'name': 'Design Phase', 'start': '2023-01-20', 'end': '2023-02-10', 'progress': 0.5},
            {'name': 'Development - Module A', 'start': '2023-02-01', 'end': '2023-02-28', 'progress': 0.3},
            {'name': 'Development - Module B', 'start': '2023-02-15', 'end': '2023-03-10', 'progress': 0.0},
            {'name': 'Testing', 'start': '2023-03-01', 'end': '2023-03-20', 'progress': 0.0},
            {'name': 'Deployment', 'start': '2023-03-25', 'end': '2023-03-30', 'progress': 0.0},
        ]
        self.gantt_chart_widget.set_tasks(sample_tasks)
