from qgis.PyQt.QtCore import QCoreApplication, QSettings, Qt
from qgis.PyQt.QtGui import QIcon, QColor, QPixmap
from qgis.PyQt.QtWidgets import QColorDialog, QToolButton
from qgis.utils import iface

import os.path

# --- CROSS-VERSION ENUM COMPATIBILITY HANDLING ---
try:
    TOOL_BUTTON_STYLE = Qt.ToolButtonStyle.ToolButtonIconOnly
    CONTEXT_MENU_POLICY = Qt.ContextMenuPolicy.CustomContextMenu
except AttributeError:
    # Fallback to the Qt5 legacy structure
    TOOL_BUTTON_STYLE = Qt.ToolButtonIconOnly
    CONTEXT_MENU_POLICY = Qt.ContextMenuPolicy.CustomContextMenu


class CanvasColour:
    """QGIS Plugin Implementation working seamlessly on both QGIS 3 and QGIS 4."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.toolbar = None
        self.buttons = {}  # Store button references structurally

        # Load global user settings or fall back to defaults
        saved_primary = QSettings().value("CanvasColour/primary_color", "#212830")
        saved_secondary = QSettings().value("CanvasColour/secondary_color", "#ffffff")
        self.primary_color = QColor(saved_primary)
        self.secondary_color = QColor(saved_secondary)

        # Load last-used color selection
        self.current_color_name = QSettings().value("CanvasColour/last_used", "primary")

    def tr(self, message):
        return QCoreApplication.translate('CanvasColour', message)

    def initGui(self):
        """Create toolbar and populate with dynamic theme switch buttons."""
        self.toolbar = self.iface.addToolBar('CanvasColour')
        self.toolbar.setObjectName('CanvasColour')

        # Dynamically build UI elements without repetitive code blocks
        for role in ["primary", "secondary"]:
            self.add_color_button(role)

        # Set the initial visual state of the canvas without modifying project data
        self.apply_canvas_visuals()

    def add_color_button(self, role):
        """Build and register a single color color swatch tool button."""
        button = QToolButton(self.toolbar)
        button.setObjectName(role)
        button.setAutoRaise(True)
        button.setCheckable(False)
        button.setToolButtonStyle(TOOL_BUTTON_STYLE)
        button.setIconSize(self.iface.iconSize())

        # Determine structural colors to apply to icons
        color = self.primary_color if role == "primary" else self.secondary_color
        self.update_button_icon(button, color)

        # Connect action slots elegantly via single-expression lambda mappings
        button.setContextMenuPolicy(CONTEXT_MENU_POLICY)
        button.customContextMenuRequested.connect(
            lambda pos, b=button: self.open_color_dialog(b)
        )
        button.clicked.connect(
            lambda _, b=button: self.set_active_color(b.objectName())
        )

        self.toolbar.addWidget(button)
        self.buttons[role] = button  # Save a reference to prevent garbage collection

    def update_button_icon(self, button, color):
        """Refresh button look with color swatch icon and a responsive tooltip."""
        size = self.iface.iconSize().width()
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        
        button.setIcon(QIcon(pixmap))
        button.setToolTip(f"{button.objectName().capitalize()} canvas color: {color.name()}")

    def open_color_dialog(self, button):
        """Handle right-click event to reconfigure a color preference slot."""
        role = button.objectName()
        current_color = self.primary_color if role == "primary" else self.secondary_color
        
        selected = QColorDialog.getColor(
            current_color, 
            self.iface.mainWindow(), 
            f"Select {role.capitalize()} Color"
        )

        if selected.isValid():
            if role == "primary":
                self.primary_color = selected
            else:
                self.secondary_color = selected

            self.update_button_icon(button, selected)
            self.save_settings()

            # Live reload canvas color immediately if updating the currently checked color
            if role == self.current_color_name:
                self.apply_canvas_visuals()

    def set_active_color(self, role):
        """Handle left-click event to swap global map viewport colors."""
        self.current_color_name = role
        self.apply_canvas_visuals()
        self.save_settings()

    def apply_canvas_visuals(self):
        """Safely push visual update to Map Canvas without dirtying QgsProject data."""
        color = self.primary_color if self.current_color_name == "primary" else self.secondary_color
        canvas = self.iface.mapCanvas()
        
        # Apply change purely to current environment instance
        canvas.setCanvasColor(color)
        canvas.refresh()
        canvas.update()

    def save_settings(self):
        """Persist settings globally to user configuration registry."""
        settings = QSettings()
        settings.setValue("CanvasColour/primary_color", self.primary_color.name())
        settings.setValue("CanvasColour/secondary_color", self.secondary_color.name())
        settings.setValue("CanvasColour/last_used", self.current_color_name)

    def unload(self):
        """Cleanly remove GUI components during plugin teardown operations."""
        if self.toolbar:
            self.toolbar.clear()  # Removes hosted widgets safely
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar.deleteLater()
            self.toolbar = None
            self.buttons.clear()

    def run(self):
        pass