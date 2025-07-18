from PySide6.QtCore import QDate, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView

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
        self.tasks = tasks_data
        self.scene.clear() # Clear existing items

        # if not self.tasks:
        #     return

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

        min_date = self.tasks[0].start_date
        max_date = self.tasks[0].end_date

        for task in self.tasks:
            if task.start_date < min_date:
                min_date = task.start_date
            if task.end_date > max_date:
                max_date = task.end_date

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
            date_text_item.setDefaultTextColor(QColor('black'))

            current_date = current_date.addDays(1)
            current_day_offset += 1

        # Draw tasks
        for i, task in enumerate(self.tasks):
            task_name = task.name
            start_date = task.start_date
            end_date = task.end_date
            progress = task.progress #0.0 (0%) to 1.0 (100%)

            # Calculate position and width of the task bar
            x_start = self.start_date.daysTo(start_date) * self.day_width # Define the position on grid of the start of the bar
            duration_days = task.get_duration_days() # Add one to include the end day
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
            text_item = self.scene.addText(task_name, task_font)
            text_item.setPos(
                x_start+5,
                y_pos+10 + (self.row_height-20
                            - text_item.boundingRect().height()
                           ) / 2
            )
            text_item.setDefaultTextColor(QColor('black'))

            # Store task ID with the graphics item for selection
            text_item.setData(0, task.id) #Store the task ID in data row 0
            bar_item = self.scene.addRect(
                bar_rect,
                QPen(Qt.NoPen),
                QBrush(Qt.NoBrush)
            )
            bar_item.setData(0, task.id)
            bar_item.setFlag(QGraphicsItem.ItemIsSelectable) #Make it selectable
            bar_item.setZValue(1) # Bring to front for selection
            text_item.setZValue(2) # Text on top of bar

    def mousePressEvent(self, event):
        """
        Handle mouse clicks to select task.
        """
        item = self.itemAt(event.pos())
        if item and item.data(0) is not None:
            # Clear previous selection
            for selected_item in self.scene.selectedItems():
                selected_item.setSelected(False)
            item.setSelected(True)
            self.selected_task_id = item.data(0)
            print(f"Selected Task ID: {self.selected_task_id}")
        else:
            self.selected_task_id = None
            for selected_item in self.scene.selectedItems():
                    selected_item.setSelected(False)
        super().mousePressEvent(event)
