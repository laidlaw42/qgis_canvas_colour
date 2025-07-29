from qgis.PyQt.QtCore import QCoreApplication, QSettings, Qt
from qgis.PyQt.QtGui import QIcon, QColor, QPixmap
from qgis.PyQt.QtWidgets import QAction, QPushButton, QColorDialog
from qgis.utils import iface

import os.path


class CanvasColour:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&CanvasColour')

        # Load settings or defaults
        saved_primary = QSettings().value("CanvasColour/primary_color", "#212830")
        saved_secondary = QSettings().value("CanvasColour/secondary_color", "#ffffff")
        self.primary_color = QColor(saved_primary)
        self.secondary_color = QColor(saved_secondary)

        # Load last-used color
        self.current_color_name = QSettings().value("CanvasColour/last_used", "primary")

        self.toolbar = self.iface.addToolBar(u'CanvasColour')
        self.toolbar.setObjectName(u'CanvasColour')

        self.add_color_button("primary")
        self.add_color_button("secondary")

        self.set_canvas_color()

    def tr(self, message):
        return QCoreApplication.translate('CanvasColour', message)

    def add_color_button(self, label):
        """Add a color button that handles left/right click."""
        button = QPushButton()
        button.setObjectName(label)
        button.setToolTip(f"{label.capitalize()} canvas color")

        if label == "primary":
            self.primary_button = button
            self.update_button_icon(button, self.primary_color)
        else:
            self.secondary_button = button
            self.update_button_icon(button, self.secondary_color)

        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(lambda pos, b=button: self.open_color_dialog(b))
        button.clicked.connect(lambda _, b=button: self.set_active_color(b.objectName()))

        self.toolbar.addWidget(button)

    def update_button_icon(self, button, color):
        """Update a button to show a color swatch icon."""
        icon = self.make_color_icon(color)
        button.setIcon(icon)
        button.setToolTip(f"{button.objectName().capitalize()}: {color.name()}")

    def make_color_icon(self, color):
        pixmap = QPixmap(40, 20)
        pixmap.fill(color)
        return QIcon(pixmap)

    def open_color_dialog(self, button):
        """Handle right-click — open color picker and update button."""
        name = button.objectName()
        current = self.primary_color if name == "primary" else self.secondary_color
        selected = QColorDialog.getColor(current, iface.mainWindow(), f"Select {name.capitalize()} Color")

        if selected.isValid():
            if name == "primary":
                self.primary_color = selected
                self.update_button_icon(button, self.primary_color)
            else:
                self.secondary_color = selected
                self.update_button_icon(button, self.secondary_color)

            self.save_settings()
            if name == self.current_color_name:
                self.set_canvas_color()  # live update if it's the current one

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
        canvas.repaint()

    def save_settings(self):
        QSettings().setValue("CanvasColour/primary_color", self.primary_color.name())
        QSettings().setValue("CanvasColour/secondary_color", self.secondary_color.name())
        QSettings().setValue("CanvasColour/last_used", self.current_color_name)

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&CanvasColour'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        pass

    def initGui(self):
        pass
