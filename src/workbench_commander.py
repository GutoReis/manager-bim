import FreeCAD
import FreeCADGui

from src.main_window import MainWindow

class ManagerBIMCommand:
    """
    The FreeCAD command executed when the button is clicked.
    It opens the custom Dock widget loading the gantt application.
    """
    def Activated(self):
        """
        Check if the gantt panel is already visible.
        If not, create a new one, if yes then proceed.
        """
        mw = FreeCADGui.getMainWindow()
        dock = mw.findChild(MainWindow, "ManagerBIM")

        if dock is None:
            self.panel = MainWindow()
            FreeCADGui.get = "ManagerBIM"
            FreeCADGui.add = "ManagerBIM"
        else:
            dock.show()

    def GetState(self):
        """
        The command is always active,
        the state 8 menas 'normal active'
        """
        return 8

    def IsActive(self):
        return True

#FreeCADGui.add = "ManagerBIMCommand"
FreeCADGui.addCommand("ManagerBimStart", ManagerBimCommand())
