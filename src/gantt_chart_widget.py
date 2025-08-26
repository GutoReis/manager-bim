from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView

class GanttChartWidget(QGraphicsView):
    """
    A GraphicView subclass to display a Gantt chart on Freecad.
    It uses a QGraphicScene to manage the graphic items (tasks).
    """
    def __init__(self, task_manager, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.task_manager = task_manager
        self.tasks = []
        self.task_graphic_items: dict[int, QGraphicsRectItem] = {}
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
        self.task_graphic_items.clear()

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
            return

        min_date = self.tasks[0].start_date
        max_date = self.tasks[0].end_date

        for task in self.tasks:
            if task.start_date < min_date:
                min_date = task.start_date
            if task.end_date > max_date:
                max_date = task.end_date

        self.start_date = min_date.addDays(-1) # Add a few days buffer at start
        self.end_date = max_date.addDays(2) # Add a few days buffer at the end

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

        # Arrows for dependency configurations
        arrow_pen = QPen(
            QColor("#888888"), # Grey Color
            1.5 # Medium Thickness
        )
        arrow_pen.setCapStyle(Qt.RoundCap) # Rounded end for lines.

        corner_radius = 4

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
            progress = task.progress #0.0 (0%) to 1.0 (100%)
            progress_str = f"{round(progress, 2) * 100}%"

            # Calculate position and width of the task bar
            x_start = self.start_date.daysTo(start_date) * self.day_width # Define the position on grid of the start of the bar
            duration_days = task.get_duration_days() # Add one to include the end day
            bar_width = duration_days * self.day_width

            y_pos = (i + 1) * self.row_height # Tasks start below date header

            # If position is different than the stored on class, save it:
            if task.x_position is None or task.x_position != x_start:
                task.x_position = x_start
            if task.y_position is None or task.y_position != y_pos:
                task.y_position = y_pos
            if task.index is None or task.index != i:
                task.index = i

            ### Draw task bar background
            bar_rect = QRectF(
                x_start,
                y_pos + 10,
                bar_width,
                self.row_height - 20
            )
            background_path = QPainterPath()
            background_path.addRoundedRect(
                bar_rect,
                corner_radius,
                corner_radius
            )
            background_item = self.scene.addPath(
                background_path,
                QPen(QColor('#cccccc')),
                QBrush(QColor('#ADD8E6'))
            )
            background_item.setData(0, task.id)
            background_item.setFlag(QGraphicsItem.ItemIsSelectable)
            background_item.setZValue(1)
            # self.scene.addRect(
            #     bar_rect,
            #     QPen(QColor('#cccccc')),
            #     QBrush(QColor('#ADD8E6'))
            # ) # Light blue

            ### Draw the progress bar
            progress_width = bar_width * progress
            progress_rect = QRectF(
                x_start,
                y_pos+10,
                progress_width,
                self.row_height - 20
            )
            progress_path = QPainterPath()
            progress_path.addRoundedRect(
                progress_rect,
                corner_radius,
                corner_radius
            )
            progress_item = self.scene.addPath(
                progress_path,
                QPen(QColor('#4682B4')),
                QBrush(QColor('#4682B4'))
            )
            progress_item.setZValue(2)
            #self.scene.addRect(
            #    progress_rect,
            #    QPen(QColor('#4682B4')),
            #    QBrush(QColor('#4682B4'))
            #) # Steel blue

            ### Add task name text
            task_font = QFont('Inter', 9)
            text_item = self.scene.addText(
                f"{task_name} - {progress_str}",
                task_font
            )

            text_item.setPos(
                x_start+5,
                y_pos+10 + (self.row_height-20
                            - text_item.boundingRect().height()
                           ) / 2
            )
            text_item.setDefaultTextColor(QColor('black'))
            # Store task ID with the graphics item for selection
            text_item.setData(0, task.id) #Store the task ID in data row 0
            highlight_path = QPainterPath()
            highlight_path.addRoundedRect(
                bar_rect,
                corner_radius,
                corner_radius
            )
            highlight_item = self.scene.addPath(
                highlight_path,
                QPen(Qt.NoPen),
                QBrush(Qt.NoBrush)
            )
            highlight_item.setData(0, task.id)
            highlight_item.setFlag(QGraphicsItem.ItemIsSelectable) #Make it selectable
            highlight_item.setZValue(3) # Bring to front for selection
            text_item.setZValue(3) # Text on top of bar
            self.task_graphic_items[task.id] = highlight_item

            ### Draw the dependency
            if task.depends_on:
                print(task.depends_on)
                # TODO: Create a method in task_item that returns
                # the dependency data for drawing the dependency
                dependent_id = int(task.depends_on.split("-")[0].strip())
                dependent_task = self.task_manager.get_task(dependent_id)

                # Calculate coordinates for the arrow
                # Arrow starts from the end of the predecessor task bar
                # Arrow ends at the start of the current task bar

                # Y position to start the line, based on the Y position
                # of the predecessor task
                start_y_arrow = dependent_task.y_position + self.row_height / 2
                # Y position to end the line, based on current task
                end_y_arrow = y_pos + self.row_height / 2

                # X position to start the line, based on the X position
                # of the predecessor task, add the bar width to set to the end of the task
                # start_x_arrow = dependent_task.x_position + bar_width
                start_x_arrow = (self.start_date.daysTo(dependent_task.end_date) + 1) * self.day_width
                # X position to start the line, based on current task
                end_x_arrow = x_start

                # Define the break L-shaped line
                horizontal_offset = 10
                vertical_offset = 10

                break_start_x = start_x_arrow + horizontal_offset
                break_start_y = start_y_arrow
                break_end_y = end_y_arrow
                break_end_x = end_x_arrow - horizontal_offset

                # Draw segments
                # From predecessor task to break
                self.scene.addLine(
                    start_x_arrow,
                    start_y_arrow,
                    break_start_x,
                    break_start_y,
                    arrow_pen
                )
                # From start of break to end of break
                self.scene.addLine(
                    break_start_x,
                    break_start_y,
                    break_end_x,
                    break_end_y,
                    arrow_pen
                )
                # From break to current task
                self.scene.addLine(
                    break_end_x,
                    break_end_y,
                    end_x_arrow,
                    end_y_arrow,
                    arrow_pen
                )
                # Arrowhead
                arrow_size = 8
                arrowhead = QPolygonF()
                arrowhead.append(QPointF(end_x_arrow, end_y_arrow))
                arrowhead.append(QPointF(
                    end_x_arrow - arrow_size,
                    end_y_arrow - arrow_size/2
                ))
                arrowhead.append(QPointF(
                    end_x_arrow - arrow_size,
                    end_y_arrow + arrow_size/2
                ))
                self.scene.addPolygon(
                    arrowhead,
                    QPen(arrow_pen.color()),
                    QBrush(arrow_pen.color())
                )

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
