from PySide6.QtCore import QDate, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

class GanttChartWidget(QGraphicsView):
    """
    A GraphicView subclass to display a Gantt chart on Freecad.
    It uses a QGraphicScene to manage the graphic items (tasks).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        #self.setRenderHint(Qt.Antialiasing) # For smoother graphics

        self.tasks = []
        self.start_date = None
        self.end_date = None
        self.day_width = 50 # Pixels per day
        self.row_height = 40 # Height of each task bar

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up a basic UI elements for the Gantt Chart.
        """
        self.setBackgroundBrush(
            QBrush(
                QColor('#f0f0f0') # Light gray background
            )
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def set_tasks(self, tasks_data):
        """
        Sets the tasks for the Gantt chart and redraws it.
        tasks_data should be a list of dictionaries:
        [
            {
                'name': 'Task A',
                'start': '2023-01-01',
                'end': '2023-01-10',
                'progress': 0.7,
                'dependens_on': none,
                'groups': 'foundation'
            },
            {
                'name': 'Task B',
                'start': '2023-01-10',
                'end': '2023-01-15',
                'progress': 0.3,
                'dependens_on': 'Task A',
                'groups': 'foundation'
            }
        ]
        """
        # TODO: REFACTOR THIS SO TASKS BECOME A CLASS
        self.tasks = tasks_data
        self.scene.clear() # Clear existing items

        if not self.tasks:
            return

        self.calculate_date_range()
        self.draw_chart()

    def calculate_date_range(self):
        """
        Calculates the overall start and end dates from the tasks.
        If no tasks on Gantt, returns the default view as 7 days ahead.
        If there are tasks, then return the start date of the first tasks
        and the end date of the last task.
        Obs.: Tasks may not be ordered by date.
        """
        if not self.tasks:
            self.start_date = QDate.currentDate()
            self.end_date = QDate.currentDate().addDays(7)
            return

        min_date = QDate.fromString(self.tasks[0]['start'], 'yyyy-MM-dd')
        max_date = QDate.fromString(self.tasks[-1]['end'], 'yyyy-MM-dd')

        for task in self.tasks:
            start = QDate.fromString(task['start'], 'yyyy-MM-dd')
            end = QDate.fromString(task['end'], 'yyyy-MM-dd')
            if start < min_date:
                min_date = start
            if end > max_date:
                max_date = end

        self.start_date = min_date.addDays(-3) # Add a few days buffer at start
        self.end_date = max_date.addDays(3) # Add a few days buffer at the end

    def draw_chart(self):
        """
        Draws the grid, date labels, and task bars on the QGraphicScene.
        If no start date or end date, returns empty view.
        """
        if not self.start_date or not self.end_date:
            return

        total_days = self.start_date.daysTo(self.end_date)
        chart_width = total_days * self.day_width
        chart_height = (len(self.tasks) + 1) * self.row_height # Add one for date header

        # Set schene rect to ensure scrollbars appear if content is larger than view
        self.scene.setSceneRect(0, 0, chart_width, chart_height)

        # Draw timeline and date labels
        current_day_offset = 0
        date_font = QFont('Inter', 8)
        date_pen = QPen(QColor('#666666'))

        current_date = self.start_date
        while current_date <= self.end_date:
            x_pos = current_day_offset * self.day_width

            # Draw vertical grid line
            self.scene.addLine(x_pos, 0 , x_pos, chart_height, QPen(QColor('#dddddd'), 0.5))

            # Draw date label
            date_text_item = self.scene.addText(current_date.toString('MMM dd'), date_font)
            date_text_item.setPos(x_pos + 5, 5) # Position slightly offset from line

            current_date = current_date.addDays(1)
            current_day_offset += 1

        # Draw tasks
        for i, task in enumerate(self.tasks):
            task_name = task.get('name', f'Unnamed Task {i+1}')
            start_date_str = task.get('start')
            end_date_str = task.get('end')
            progress = task.get('progress', 0.0) #0.0 (0%) to 1.0 (100%)

            if not start_date_str or not end_date_str:
                continue

            start_date = QDate.fromString(start_date_str, 'yyyy-MM-dd')
            end_date = QDate.fromString(end_date_str, 'yyyy-MM-dd')

            if not start_date.isValid() or not end_date.isValid():
                continue

            # Calculate position and width of the task bar
            x_start = self.start_date.daysTo(start_date) * self.day_width # Define the position on grid of the start of the bar
            duration_days = start_date.daysTo(end_date) + 1 # Add one to include the end day
            bar_width = duration_days * self.day_width

            y_pos = (i + 1) * self.row_height # Tasks start below date header

            # Draw task bar background
            bar_rect = QRectF(
                x_start,
                y_pos + 10,
                bar_width,
                self.row_height - 20
            )
            self.scene.addRect(
                bar_rect,
                QPen(QColor('#cccccc')),
                QBrush(QColor('#ADD8E6'))
            ) # Light blue

            # Draw the progress bar
            progress_width = bar_width * progress
            progress_rect = QRectF(
                x_start,
                y_pos+10,
                progress_width,
                self.row_height - 20
            )
            self.scene.addRect(
                progress_rect,
                QPen(QColor('#4682B4')),
                QBrush(QColor('#4682B4'))
            ) # Steel blue

            # Add task name text
            task_font = QFont('Inter', 9)
            task_item = self.scene.addText(task_name, task_font)
            task_item.setPos(
                x_start+5,
                y_pos+10 + (self.row_height-20
                            - task_item.boundingRect().height()
                           ) / 2
            )
            task_item.setDefaultTextColor(QColor('black'))
