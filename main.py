import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow,
    QSlider, QLabel, QHBoxLayout, QColorDialog
)
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

# ===== 定数定義 =====
ALLOWED_SIZES = [10, 14, 18, 22, 26, 30]  # 許容されるクロスヘアサイズ
ALLOWED_THICKNESS = [1, 2, 3]             # 許容される線の太さ
DEFAULT_SIZE = 14                         # デフォルトサイズ
DEFAULT_THICKNESS = 2                    # デフォルトの太さ
DEFAULT_COLOR = QColor(0, 255, 255)      # デフォルト色（シアン）

WINDOW_TITLE = "Reticore Control"
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 160

BUTTON_MIN_HEIGHT = 40
COLOR_BUTTON_WIDTH = 40
SPACING_BETWEEN_ROWS = 8

SLIDER_STEP_SIZE = 4
THICKNESS_STEP_SIZE = 1

class CrosshairOverlay(QWidget):
    """
    クロスヘア（十字線）を画面中央に表示する透過ウィンドウ。

    Attributes:
        size (int): クロスヘアのサイズ（縦横）
        thickness (int): 線の太さ
        color (QColor): クロスヘアの色
    """
    def __init__(self, size=DEFAULT_SIZE, thickness=DEFAULT_THICKNESS, color=DEFAULT_COLOR):
        super().__init__()
        self.size = size
        self.thickness = thickness
        self.color = color

        # ウィンドウ設定（フレームレス・最前面・ツール扱い・透過）
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.move_to_center()

    def move_to_center(self):
        """画面の中央にクロスヘアを配置する。"""
        screen = QApplication.primaryScreen().geometry()
        center_x = screen.left() + screen.width() // 2
        center_y = screen.top() + screen.height() // 2
        left = center_x - self.size // 2
        top = center_y - self.size // 2
        self.setGeometry(left, top, self.size, self.size)

    def update_crosshair(self, size, thickness, color):
        """
        クロスヘアの見た目を更新する。

        Args:
            size (int): 新しいサイズ
            thickness (int): 新しい線の太さ
            color (QColor): 新しい色
        """
        self.size = size
        self.thickness = thickness
        self.color = color
        self.move_to_center()
        self.update()

    def paintEvent(self, event):
        """クロスヘア（十字線）を描画する。"""
        painter = QPainter(self)
        pen = QPen(self.color)
        pen.setWidth(self.thickness)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setPen(pen)
        center = self.size // 2
        painter.drawLine(center, 0, center, self.size)     # 縦線
        painter.drawLine(0, center, self.size, center)     # 横線

class MainWindow(QMainWindow):
    """
    クロスヘアのオン/オフ、サイズ・太さ・色の設定を行うGUIウィンドウ。
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.crosshair = None

        # --- サイズスライダー設定 ---
        self.size_label = QLabel(f"Size: {DEFAULT_SIZE}")
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(min(ALLOWED_SIZES))
        self.size_slider.setMaximum(max(ALLOWED_SIZES))
        self.size_slider.setValue(DEFAULT_SIZE)
        self.size_slider.setSingleStep(SLIDER_STEP_SIZE)
        self.size_slider.setPageStep(SLIDER_STEP_SIZE)
        self.size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.size_slider.setTickInterval(SLIDER_STEP_SIZE)
        self.size_slider.valueChanged.connect(self.on_size_changed)

        # --- 太さスライダー設定 ---
        self.thick_label = QLabel(f"Thickness: {DEFAULT_THICKNESS}")
        self.thick_slider = QSlider(Qt.Orientation.Horizontal)
        self.thick_slider.setMinimum(min(ALLOWED_THICKNESS))
        self.thick_slider.setMaximum(max(ALLOWED_THICKNESS))
        self.thick_slider.setValue(DEFAULT_THICKNESS)
        self.thick_slider.setSingleStep(THICKNESS_STEP_SIZE)
        self.thick_slider.setPageStep(THICKNESS_STEP_SIZE)
        self.thick_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.thick_slider.setTickInterval(THICKNESS_STEP_SIZE)
        self.thick_slider.valueChanged.connect(self.on_thick_changed)

        # --- 色選択ボタン設定 ---
        self.color = DEFAULT_COLOR
        self.color_button = QPushButton()
        self.color_button.setFixedWidth(COLOR_BUTTON_WIDTH)
        self.update_color_button()
        self.color_button.clicked.connect(self.open_color_picker)
        self.color_label = QLabel("Color:")

        # --- トグルボタン（有効/無効） ---
        self.toggle_button = QPushButton("Enable")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setMinimumHeight(BUTTON_MIN_HEIGHT)
        self.toggle_button.clicked.connect(self.toggle_crosshair)

        # --- レイアウト構築 ---
        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addSpacing(SPACING_BETWEEN_ROWS)

        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_slider)
        layout.addLayout(size_layout)
        layout.addSpacing(SPACING_BETWEEN_ROWS)

        thick_layout = QHBoxLayout()
        thick_layout.addWidget(self.thick_label)
        thick_layout.addWidget(self.thick_slider)
        layout.addLayout(thick_layout)
        layout.addSpacing(SPACING_BETWEEN_ROWS)

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
        """色ボタンの背景を現在選択中の色に更新する。"""
        c = self.color
        self.color_button.setStyleSheet(
            f"background-color: rgb({c.red()},{c.green()},{c.blue()});"
        )

    def open_color_picker(self):
        """カラーピッカーを表示し、選択された色を反映する。"""
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
        """
        トグルボタンによってクロスヘアを表示または非表示に切り替える。

        Args:
            checked (bool): True = 表示、False = 非表示
        """
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
        """
        サイズスライダーの値変更時に呼び出され、最も近い許容サイズにスナップして更新する。

        Args:
            value (int): スライダーで設定されたサイズ値
        """
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
        """
        太さスライダーの値変更時に呼び出され、最も近い許容太さにスナップして更新する。

        Args:
            value (int): スライダーで設定された太さ
        """
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
        """ウィンドウを閉じるときにクロスヘアを一緒に閉じる。"""
        if self.crosshair:
            self.crosshair.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
