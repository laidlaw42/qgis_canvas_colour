from qgis.PyQt.QtCore import QCoreApplication, QSettings, Qt
from qgis.PyQt.QtGui import QIcon, QColor, QPixmap
from qgis.PyQt.QtWidgets import QPushButton, QColorDialog, QToolButton
from qgis.utils import iface
from qgis.core import QgsProject

import os.path

# --- CROSS-VERSION ENUM COMPATIBILITY HANDLING ---
# PyQt6 (QGIS 4) introduces rigid namespace scoping for Enums, 
# while PyQt5 (QGIS 3) expects flat, direct calls.
try:
    TOOL_BUTTON_STYLE = Qt.ToolButtonStyle.ToolButtonIconOnly
    CONTEXT_MENU_POLICY = Qt.ContextMenuPolicy.CustomContextMenu
except AttributeError:
    # Fallback to the Qt5 legacy structure
    TOOL_BUTTON_STYLE = Qt.ToolButtonIconOnly
    CONTEXT_MENU_POLICY = Qt.CustomContextMenu


class CanvasColour:
    """QGIS Plugin Implementation working on both QGIS 3 and QGIS 4."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr('&CanvasColour')

        # Load settings or defaults
        saved_primary = QSettings().value("CanvasColour/primary_color", "#212830")
        saved_secondary = QSettings().value("CanvasColour/secondary_color", "#ffffff")
        self.primary_color = QColor(saved_primary)
        self.secondary_color = QColor(saved_secondary)

        # Load last-used color
        self.current_color_name = QSettings().value("CanvasColour/last_used", "primary")
        self.toolbar = None

    def tr(self, message):
        return QCoreApplication.translate('CanvasColour', message)

    def initGui(self):
        self.toolbar = self.iface.addToolBar('CanvasColour')
        self.toolbar.setObjectName('CanvasColour')

        self.add_color_button("primary")
        self.add_color_button("secondary")

        self.set_canvas_color()

    def add_color_button(self, label):
        button = QToolButton(self.toolbar)
        button.setObjectName(label)

        button.setAutoRaise(True)
        button.setCheckable(False)
        button.setToolButtonStyle(TOOL_BUTTON_STYLE) # Version-safe styling
        button.setIconSize(self.iface.iconSize())

        button.setToolTip(f"{label.capitalize()} canvas color")

        if label == "primary":
            self.primary_button = button
            self.update_button_icon(button, self.primary_color)
        else:
            self.secondary_button = button
            self.update_button_icon(button, self.secondary_color)

        button.setContextMenuPolicy(CONTEXT_MENU_POLICY) # Version-safe policy
        
        button.customContextMenuRequested.connect(
            lambda pos, b=button: self.open_color_dialog(b)
        )
        button.clicked.connect(
            lambda _, b=button: self.set_active_color(b.objectName())
        )

        self.toolbar.addWidget(button)

    def update_button_icon(self, button, color):
        """Update a button to show a color swatch icon."""
        icon = self.make_color_icon(color)
        button.setIcon(icon)
        button.setToolTip(f"{button.objectName().capitalize()}: {color.name()}")

    def make_color_icon(self, color):
        size = self.iface.iconSize().width()
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        return QIcon(pixmap)

    def open_color_dialog(self, button):
        """Handle right-click — open color picker and update button."""
        name = button.objectName()
        current = self.primary_color if name == "primary" else self.secondary_color
        selected = QColorDialog.getColor(current, self.iface.mainWindow(), f"Select {name.capitalize()} Color")

        if selected.isValid():
            if name == "primary":
                self.primary_color = selected
                self.update_button_icon(button, self.primary_color)
            else:
                self.secondary_color = selected
                self.update_button_icon(button, self.secondary_color)

            self.save_settings()
            if name == self.current_color_name:
                self.set_canvas_color()

    def set_active_color(self, name):
        """Handle left-click — set canvas background to selected button’s color."""
        self.current_color_name = name
        self.set_canvas_color()
        self.save_settings()

    def set_canvas_color(self):
        """Apply current active color to map canvas."""
        color = self.primary_color if self.current_color_name == "primary" else self.secondary_color
        canvas = self.iface.mapCanvas()
        
        canvas.setCanvasColor(color)
        canvas.refresh()
        canvas.update()
        
        # This API has been highly stable and identical across both versions!
        project = QgsProject.instance()
        project.writeEntry("Gui", "/CanvasColorRedPart", color.red())
        project.writeEntry("Gui", "/CanvasColorGreenPart", color.green())
        project.writeEntry("Gui", "/CanvasColorBluePart", color.blue())

    def save_settings(self):
        QSettings().setValue("CanvasColour/primary_color", self.primary_color.name())
        QSettings().setValue("CanvasColour/secondary_color", self.secondary_color.name())
        QSettings().setValue("CanvasColour/last_used", self.current_color_name)

    def unload(self):
        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            del self.toolbar

    def run(self):
        pass