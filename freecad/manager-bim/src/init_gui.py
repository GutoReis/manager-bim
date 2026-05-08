import os

import FreeCADGui

_ADDON_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ICON = os.path.join(_ADDON_ROOT, "Resources", "Icons", "logo_ManagerBIM.svg")

class ManagerBIMWorkbench(FreeCADGui.Workbench):
    MenuText = "ManagerBIM"
    ToolTip = "Manager BIM is a Freecad dedicated workbench that allow a Building project to be managed."
    Icon = _ICON

    def Initialize(self):
        from . import Commands
        self.appendToolbar("ManagerBIM", ["open_panel"])
        self.appendMenu("ManagerBIM", ["open_panel"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(ManagerBIMWorkbench())
