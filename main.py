from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPixmap, QColor, QPen, QIcon, QWheelEvent, QCursor
import sys
import platform
import logging

logger = logging.getLogger(__name__)


class CursorProjectionWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        
        # macOS specific configurations
        if platform.system() == "Darwin":
            # macOS specific window flags
            self.setWindowFlags(
                Qt.WindowStaysOnTopHint | 
                Qt.Window | 
                Qt.FramelessWindowHint
            )
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # On macOS, account for menu bar and dock
        if platform.system() == "Darwin":
            available_geometry = screen.availableGeometry()
            self.setGeometry(
                available_geometry.width() // 2, 
                available_geometry.y(), 
                available_geometry.width() // 2, 
                available_geometry.height()
            )
        else:
            self.setGeometry(screen_width // 2, 0, screen_width // 2, screen_height)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Redrawing Master")
        self.setWindowIcon(QIcon("logo.png"))
        
        self.image = QPixmap(image_path)
        if self.image.isNull():
            raise ValueError(f"Couldn't load image from path: {image_path}")
        
        self.setMinimumSize(200, 200)
        
        # Timer for cursor tracking
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(30)
        
        self.cursor_x = 0
        self.cursor_y = 0
        self.clipboard = QApplication.clipboard()
        
        # On macOS, clipboard events don't work reliably for inactive windows
        # So we use polling instead
        if platform.system() == "Darwin":
            self.clipboard_timer = QTimer()
            self.clipboard_timer.timeout.connect(self.check_clipboard_macos)
            self.clipboard_timer.start(200)  # Check every 200ms - good balance
            self.last_clipboard_hash = None
        else:
            self.clipboard.dataChanged.connect(self.on_clipboard_change)
            
        self.scale_factor = 1.0
        self.radius = 10
        self.image_offset = QPoint(0, 0)
        self.dragging = False
        self.drag_start_pos = QPoint(0, 0)
        self.image_start_offset = QPoint(0, 0)
        
        # macOS specific settings
        if platform.system() == "Darwin":
            # Allow window to receive focus for clipboard access
            self.setAttribute(Qt.WA_ShowWithoutActivating, False)
            # Force window to be active initially
            QTimer.singleShot(100, self.force_activate_window)

    def update_cursor_position(self):
        try:
            global_pos = QCursor.pos()
            self.cursor_x = global_pos.x()
            self.cursor_y = global_pos.y()
            self.update()
        except Exception as e:
            logger.exception("Failed to get cursor position - accessibility permissions may be required")

    def check_clipboard_macos(self):
        """Check clipboard for new images on macOS (polling method)."""
        try:
            mime_data = self.clipboard.mimeData()
            
            if mime_data and mime_data.hasImage():
                clipboard_image = self.clipboard.image()
                if not clipboard_image.isNull():
                    # Create a hash of the image data for comparison
                    image_bytes = clipboard_image.bits().asstring(clipboard_image.byteCount())
                    current_hash = hash(image_bytes)
                    
                    if current_hash != self.last_clipboard_hash:
                        self.last_clipboard_hash = current_hash
                        self.image = QPixmap.fromImage(clipboard_image)
                        self.update()
                        logger.info("Clipboard image updated automatically on macOS")
                        
        except Exception as e:
            logger.exception("Error checking clipboard on macOS")

    def on_clipboard_change(self):
        """Handle clipboard changes on non-macOS platforms."""
        if self.clipboard.mimeData().hasImage():
            clipboard_image = self.clipboard.image()
            if not clipboard_image.isNull():
                self.image = QPixmap.fromImage(clipboard_image)
                self.update()
                logger.info("Clipboard image updated")

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

        # Get screen dimensions, accounting for macOS menu bar and dock
        screen = QApplication.primaryScreen()
        if platform.system() == "Darwin":
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
        else:
            screen_geometry = screen.geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

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
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        # Cmd+V or Ctrl+V to manually check clipboard
        if (event.key() == Qt.Key_V and 
            (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier)):
            self.force_clipboard_check()
        super().keyPressEvent(event)
    
    def force_activate_window(self):
        """Force window activation on macOS."""
        if platform.system() == "Darwin":
            self.raise_()
            self.activateWindow()
            self.setFocus()
            logger.info("Window activated for clipboard access on macOS")
    
    def force_clipboard_check(self):
        """Manually check and update from clipboard."""
        try:
            # Fallback to PyQt5 method
            if self.clipboard.mimeData().hasImage():
                clipboard_image = self.clipboard.image()
                if not clipboard_image.isNull():
                    self.image = QPixmap.fromImage(clipboard_image)
                    self.update()
                    logger.info("Manually updated image from clipboard")
        except Exception as e:
            logger.exception("Error manually checking clipboard")


def main():
    # Setup High DPI BEFORE creating QApplication
    if platform.system() == "Darwin":
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # macOS specific app configurations
    if platform.system() == "Darwin":
        # Prevent app from quitting when all windows are closed on macOS
        app.setQuitOnLastWindowClosed(False)
        # Set app name for macOS menu bar
        app.setApplicationName("Redrawing Master")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("Redrawing Master")
    
    app.setWindowIcon(QIcon("logo.png"))
    
    try:
        window = CursorProjectionWindow("gojo.png")
    except ValueError as e:
        logger.error(f"Failed to initialize window: {e}")
        if platform.system() == "Darwin":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Failed to load image")
            msg.setInformativeText(str(e))
            msg.exec_()
        else:
            print(e)
        sys.exit(1)
    
    window.show()
    
    # On macOS, bring window to front
    if platform.system() == "Darwin":
        window.raise_()
        window.activateWindow()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
