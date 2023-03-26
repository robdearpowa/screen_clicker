import sys
import os
import time
import pyautogui

from PySide2.QtWidgets import *
from PySide2.QtCore import QObject, QEvent
from PySide2.QtGui import QPicture
from PySide2.QtUiTools import QUiLoader
from PIL import ImageQt

from threading import Thread

class WindowManager(QObject):
    def __init__(self, window: QMainWindow, on_close) -> None:
        super(WindowManager, self).__init__()
        self.window = window
        self.on_close = on_close
        
    def eventFilter(self, watched, event) -> bool:
        if watched is self.window and event.type() == QEvent.Close:
            self.on_close()
            event.ignore()
            return True
        
        return super(WindowManager, self).eventFilter(watched, event)

class App(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super(App, self).__init__(argv)
        self.running = False
        
        ui_loader = QUiLoader()
        self.window: QMainWindow = ui_loader.load("screen_clicker.ui")
        self.window_manager: WindowManager = WindowManager(self.window, self.on_close)
        
        self.btn_scan: QPushButton = self.window.findChild(QPushButton, "btn_scan")
        self.btn_stop: QPushButton = self.window.findChild(QPushButton, "btn_stop")
        
        self.sbx_x: QSpinBox = self.window.findChild(QSpinBox, "sbx_x")
        self.sbx_y: QSpinBox = self.window.findChild(QSpinBox, "sbx_y")
        self.sbx_width: QSpinBox = self.window.findChild(QSpinBox, "sbx_width")
        self.sbx_height: QSpinBox = self.window.findChild(QSpinBox, "sbx_height")
    
        self.lbl_image: QLabel = self.window.findChild(QLabel, "lbl_image")
        pass
    
    def start(self) -> None:
        self.window.installEventFilter(self.window_manager)
        
        self.btn_scan.clicked.connect(self.start_scan_thread)
        self.btn_stop.clicked.connect(self.stop_scan)
        
        self.window.show()
        sys.exit(self.exec_())
        pass
    
    def start_scan_thread(self) -> None:
        scan_thread = Thread(target=self.start_scan)
        scan_thread.start()
        pass
    
    def start_scan(self) -> None:
        self.running = True
        while self.running:
            self.scan()
            time.sleep(0.16)
        pass
    
    def stop_scan(self) -> None:
        self.running = False
        pass
    
    def scan(self) -> None:
        x = self.sbx_x.value()
        y = self.sbx_y.value()
        width = self.sbx_width.value()
        height = self.sbx_height.value()
        
        before = time.time()
        screen = pyautogui.screenshot(region=(x, y, width, height))
        
        piximap = ImageQt.toqpixmap(screen)
        self.lbl_image.setPixmap(piximap)
        now = time.time()
        print(f"Frametime: {now - before}")
        pass
    
    def on_close(self) -> None:
        self.stop_scan()
        
        self.window.removeEventFilter(self.window_manager)
        self.quit()
        pass
    
if __name__ == "__main__":
    app = App(sys.argv)
    app.start()
    pass