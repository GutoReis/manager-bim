import FreeCADGui

class OpenPanelCommand:
    def GetResources(self):
        return {
            'Pixmap': 'logo_ManagerBIM', 
            'MenuText': 'Open Manager BIM Panel', 
            'ToolTip': 'Opens the Gantt chart panel'
        }

    def Activated(self):
        # Import the main window from the src module
        from .src.main_window import MainWindow
        self.window = MainWindow()
        self.window.show()

FreeCADGui.addCommand('open_panel', OpenPanelCommand())
