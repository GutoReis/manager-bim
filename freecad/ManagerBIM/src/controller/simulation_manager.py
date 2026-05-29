from PySide6.QtCore import QTimer, Qt, QPointF
from PySide6.QtGui import QColor, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsRectItem, QGraphicsPolygonItem

class SimulationManager:
    def __init__(self, gantt_widget, task_manager):
        self.gantt_widget = gantt_widget
        self.task_manager = task_manager

        # Simulation properties
        self.simulation_speed_ms = 100
        self.pipe_movement_per_tick = self.gantt_widget.day_width / 10

        # QTimer for simulation
        self.simulation_timer = QTimer(self.gantt_widget)
        self.simulation_timer.setInterval(self.simulation_speed_ms)
        self.simulation_timer.timeout.connect(self.simulation_pipe_step)

        # Visual pipe indication
        self.pipe_item = None
        self.create_pipe_item()

        # Keep track of highlighted items to easily revert them
        self.highlighted_items = []
        self.original_item_styles = {}

        self.current_simulation_x = 0.0

    def create_pipe_item(self):
        """
        Initializes the visual 'pipe' item.
        """
        pipe_width = 5

        self.pipe_item = self.gantt_widget.scene.addRect(
            0,
            0,
            pipe_width,
            self.gantt_widget.scene.sceneRect().height(),
            QPen(Qt.NoPen),
            QBrush(QColor(255, 0 , 0, 150))
        )
        self.pipe_item.setZValue(9999)
        self.pipe_item.hide()

    def update_pipe_height(self):
        """
        Adjusts the pipe's height to match the current scene height.
        """
        if self.pipe_item:
            rect = self.pipe_item.rect()
            rect.setHeight(self.gantt_widget.scene.sceneRect().height())
            self.pipe_item.setRect(rect)

    def simulation_pipe_step(self):
        """
        Moves the pipe and updates task highlights based on its position.
        """
        self.current_simulation_x += self.pipe_movement_per_tick
        self.update_pipe_height()
        self.pipe_item.setX(self.current_simulation_x)

        # Ensure the pipe is visible in the view
        # Scroll when the pipe is 25% from edge
        scroll_margin_x = self.gantt_widget.viewport().width() * 0.25
        scroll_margin_y = 0 # No need for vertical scroll
        self.gantt_widget.ensureVisible(
            self.pipe_item,
            scroll_margin_x,
            scroll_margin_y
        )

        # Stop condition
        if self.current_simulation_x >= self.gantt_widget.scene.sceneRect().width():
            self.stop_simulation()
            return

        self.clear_highlights()

        # Highlight tasks
        for task in self.task_manager.get_all_tasks():
            # Get the graphics item for the task
            task_graphic_item = self.gantt_widget.task_graphic_items.get(task.id)

            if task_graphic_item:
                # Calculate ask bar's current x range in scene coordinates
                task_rect = task_graphic_item.mapToScene(
                    task_graphic_item.boundingRect()
                ).boundingRect()
                task_x_start = task_rect.x()
                task_x_end = task_x_start + task_rect.width()

                # Check if pipe's center is over the task
                pipe_center_x = self.pipe_item.x() + (self.pipe_item.rect().width() / 2)

                if task_x_start <= pipe_center_x <= task_x_end:
                    # Apply highlight
                    self.original_item_styles[task.id] = {
                        "pen": task_graphic_item.pen(),
                        "brush": task_graphic_item.brush()
                    }
                    task_graphic_item.setPen(
                        QPen(QColor("orange"),2)
                    )
                    task_graphic_item.setBrush(
                        QBrush(QColor(255, 165, 0, 150))
                    )
                    self.highlighted_items.append(task_graphic_item)

    def clear_highlights(self):
        """
        Reverts the appearance of all currently highlighted items.
        """
        for item in self.highlighted_items:
            task_id = item.data(0)
            if task_id in self.original_item_styles:
                item.setPen(self.original_item_styles[task_id]["pen"])
                item.setBrush(self.original_item_styles[task_id]["brush"])
        self.highlighted_items.clear()
        self.original_item_styles.clear()

    def start_simulation(self):
        """
        Start the simulation pipe.
        """
        if not self.task_manager.get_all_tasks():
            print("No tasks to simulate")
            return

        self.current_simulation_x = 0.0
        self.create_pipe_item()
        self.update_pipe_height()
        self.pipe_item.setX(self.current_simulation_x)
        self.pipe_item.show()
        self.clear_highlights()
        self.simulation_timer.start()

    def stop_simulation(self):
        """
        Stops the simulation and resets the pipe.
        """
        self.simulation_timer.stop()
        self.pipe_item.hide()
        self.clear_highlights()
        self.current_simulation_x = 0.0
