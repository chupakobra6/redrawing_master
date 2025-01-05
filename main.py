from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPixmap, QColor, QPen, QIcon, QWheelEvent, QCursor
import sys


class CursorProjectionWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.setGeometry(screen_width // 2, 0, screen_width // 2, screen_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Redrawing Master")
        self.setWindowIcon(QIcon("logo.png"))
        self.image = QPixmap(image_path)
        if self.image.isNull():
            raise ValueError(f"Couldn't load image from path: {image_path}")
        self.setMinimumSize(200, 200)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(30)
        self.cursor_x = 0
        self.cursor_y = 0
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        self.scale_factor = 1.0
        self.radius = 10
        self.image_offset = QPoint(0, 0)
        self.dragging = False
        self.drag_start_pos = QPoint(0, 0)
        self.image_start_offset = QPoint(0, 0)

    def update_cursor_position(self):
        global_pos = QCursor.pos()
        self.cursor_x = global_pos.x()
        self.cursor_y = global_pos.y()
        self.update()

    def on_clipboard_change(self):
        if self.clipboard.mimeData().hasImage():
            clipboard_image = self.clipboard.image()
            if not clipboard_image.isNull():
                self.image = QPixmap.fromImage(clipboard_image)
                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setOpacity(0.5)

        new_width = int(self.size().width() * self.scale_factor)
        new_height = int(self.size().height() * self.scale_factor)

        new_width = max(1, new_width)
        new_height = max(1, new_height)

        scaled_image = self.image.scaled(
            new_width,
            new_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x = (self.width() - scaled_image.width()) / 2 + self.image_offset.x()
        y = (self.height() - scaled_image.height()) / 2 + self.image_offset.y()
        painter.drawPixmap(int(x), int(y), scaled_image)

        screen_width = QApplication.primaryScreen().geometry().width()
        screen_height = QApplication.primaryScreen().geometry().height()

        relative_x = self.cursor_x / (screen_width / 2)
        relative_y = self.cursor_y / screen_height

        relative_x = max(0.0, min(1.0, relative_x))
        relative_y = max(0.0, min(1.0, relative_y))

        projection_x = relative_x * self.width()
        projection_y = relative_y * self.height()

        pen = QPen(QColor(255, 0, 0), 3)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(QPoint(int(projection_x), int(projection_y)), self.radius, self.radius)

    def resizeEvent(self, event):
        self.update()
        super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.radius += 1
            else:
                self.radius -= 1
            self.radius = max(1, min(self.radius, 100))
        else:
            angle = event.angleDelta().y()
            if angle > 0:
                self.scale_factor *= 1.1
            else:
                self.scale_factor /= 1.1
            self.scale_factor = max(0.1, min(self.scale_factor, 10.0))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()
            self.image_start_offset = QPoint(self.image_offset)

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.drag_start_pos
            self.image_offset = self.image_start_offset + delta
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setWindowIcon(QIcon("logo.png"))
    try:
        window = CursorProjectionWindow("gojo.png")
    except ValueError as e:
        print(e)
        sys.exit(1)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
