import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow, QSlider, QLabel, QHBoxLayout, QColorDialog
)
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

# ===== Constants =====
ALLOWED_SIZES = [10, 14, 18, 22, 26, 30]
ALLOWED_THICKNESS = [1, 2, 3]
DEFAULT_SIZE = 14
DEFAULT_THICKNESS = 2
DEFAULT_COLOR = QColor(0, 255, 255)  # Cyan
WINDOW_TITLE = "Crosshair Control"
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 260

class CrosshairOverlay(QWidget):
    def __init__(self, size=DEFAULT_SIZE, thickness=DEFAULT_THICKNESS, color=DEFAULT_COLOR):
        super().__init__()
        self.size = size
        self.thickness = thickness
        self.color = color
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.move_to_center()

    def move_to_center(self):
        screen = QApplication.primaryScreen().geometry()
        center_x = screen.left() + screen.width() // 2
        center_y = screen.top() + screen.height() // 2
        left = center_x - self.size // 2
        top = center_y - self.size // 2
        self.setGeometry(left, top, self.size, self.size)

    def update_crosshair(self, size, thickness, color):
        self.size = size
        self.thickness = thickness
        self.color = color
        self.move_to_center()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(self.color)
        pen.setWidth(self.thickness)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setPen(pen)
        center = self.size // 2
        painter.drawLine(center, 0, center, self.size)
        painter.drawLine(0, center, self.size, center)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.crosshair = None

        self.size_label = QLabel(f"Size: {DEFAULT_SIZE}")
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(min(ALLOWED_SIZES))
        self.size_slider.setMaximum(max(ALLOWED_SIZES))
        self.size_slider.setValue(DEFAULT_SIZE)
        self.size_slider.setSingleStep(4)
        self.size_slider.setPageStep(4)
        self.size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.size_slider.setTickInterval(4)
        self.size_slider.valueChanged.connect(self.on_size_changed)

        self.thick_label = QLabel(f"Thickness: {DEFAULT_THICKNESS}")
        self.thick_slider = QSlider(Qt.Orientation.Horizontal)
        self.thick_slider.setMinimum(min(ALLOWED_THICKNESS))
        self.thick_slider.setMaximum(max(ALLOWED_THICKNESS))
        self.thick_slider.setValue(DEFAULT_THICKNESS)
        self.thick_slider.setSingleStep(1)
        self.thick_slider.setPageStep(1)
        self.thick_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.thick_slider.setTickInterval(1)
        self.thick_slider.valueChanged.connect(self.on_thick_changed)

        self.color = DEFAULT_COLOR
        self.color_button = QPushButton()
        self.color_button.setFixedWidth(40)
        self.update_color_button()
        self.color_button.clicked.connect(self.open_color_picker)

        self.color_label = QLabel("Color:")

        self.toggle_button = QPushButton("Enable")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_crosshair)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)

        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_slider)
        layout.addLayout(size_layout)

        thick_layout = QHBoxLayout()
        thick_layout.addWidget(self.thick_label)
        thick_layout.addWidget(self.thick_slider)
        layout.addLayout(thick_layout)

        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_label)
        color_layout.addWidget(self.color_button)
        layout.addLayout(color_layout)

        layout.addStretch()
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.current_size = DEFAULT_SIZE
        self.current_thickness = DEFAULT_THICKNESS

    def update_color_button(self):
        c = self.color
        self.color_button.setStyleSheet(
            f"background-color: rgb({c.red()},{c.green()},{c.blue()});"
        )

    def open_color_picker(self):
        color = QColorDialog.getColor(initial=self.color, parent=self)
        if color.isValid():
            self.color = color
            self.update_color_button()
            if self.crosshair:
                self.crosshair.update_crosshair(
                    size=self.current_size,
                    thickness=self.current_thickness,
                    color=self.color
                )

    def toggle_crosshair(self, checked):
        if checked:
            self.crosshair = CrosshairOverlay(
                size=self.current_size,
                thickness=self.current_thickness,
                color=self.color
            )
            self.crosshair.show()
            self.toggle_button.setText("Disable")
        else:
            if self.crosshair:
                self.crosshair.close()
                self.crosshair = None
            self.toggle_button.setText("Enable")

    def on_size_changed(self, value):
        corrected = min(ALLOWED_SIZES, key=lambda x: abs(x - value))
        if value != corrected:
            self.size_slider.blockSignals(True)
            self.size_slider.setValue(corrected)
            self.size_slider.blockSignals(False)
            value = corrected
        self.size_label.setText(f"Size: {value}")
        self.current_size = value
        if self.crosshair:
            self.crosshair.update_crosshair(
                size=value,
                thickness=self.current_thickness,
                color=self.color
            )

    def on_thick_changed(self, value):
        corrected = min(ALLOWED_THICKNESS, key=lambda x: abs(x - value))
        if value != corrected:
            self.thick_slider.blockSignals(True)
            self.thick_slider.setValue(corrected)
            self.thick_slider.blockSignals(False)
            value = corrected
        self.thick_label.setText(f"Thickness: {value}")
        self.current_thickness = value
        if self.crosshair:
            self.crosshair.update_crosshair(
                size=self.current_size,
                thickness=value,
                color=self.color
            )

    def closeEvent(self, event):
        if self.crosshair:
            self.crosshair.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
