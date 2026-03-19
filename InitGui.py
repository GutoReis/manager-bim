from pathlib import Path

import FreeCAD as App
import FreeCADGui

# from FreeCADGui import Workbench


class ManagerBIMWorkbench(FreeCADGui.Workbench):
    """
    Defines the FreeCAD Workbench structure.
    """

    ICON_PATH = Path(App.getResourceDir()) / "Mod" / "manager-bim" / "src" / "assets" / "logo_ManagerBIM.svg"
    Icon = str(ICON_PATH)
    MenuText = "ManagerBIM Workbench"
    ToolTip = "Bancada dedicada para BIM 4D"

    def Initialize(self):
        """
        This function is executed when FreeCAD starts.
        """
        import src.workbench_commander

        self.appendMenu("ManagerBIM", ["ManagerBimStart"])

    def Activated(self):
        """
        This function is executed when the workbench is actived
        """
        pass

    def Deactivated(self):
        """
        This function is executed when the workbench is deactivated.
        """
        pass

    def GetClassName(self):
        return "ManagerBIMWorkbench"


FreeCADGui.addWorkbench(ManagerBIMWorkbench())
