from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget)

from .view.gantt_chart_widget import GanttChartWidget
from .controller.simulation_manager import SimulationManager
from .controller.task_manager import TaskManager
from .view.toolbar import Toolbar

class MainWindow(QMainWindow):
#class MainWindow(QWidget):
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

        self.gantt_chart_widget = GanttChartWidget(parent=self, task_manager=self.task_manager)
        layout.addWidget(self.gantt_chart_widget)

        self.simulation_manager = SimulationManager(self.gantt_chart_widget, self.task_manager)

        self.toolbar = Toolbar(main_window=self)
        self.addToolBar(self.toolbar.toolbar)
        self.refresh_gantt_chart()

    def refresh_gantt_chart(self):
        """
        Refreshes the Gantt chart with the latest data from TaskManager.
        """
        self.gantt_chart_widget.set_tasks(self.task_manager.get_all_tasks())
