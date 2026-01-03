import sys
import time
import threading
import requests

from PyQt5.QtWidgets import (QVBoxLayout,QHBoxLayout,QWidget,QApplication,QPushButton,QLabel,QMessageBox)
from PyQt5.QtGui import QPalette ,QColor , QFont
from PyQt5.QtCore import Qt,pyqtSignal

SERVER_URL = "http://127.0.0.1:8000"

class SpeedTestApp(QWidget):
    update_label = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Test")
        self.setGeometry(300,200,400,300)

        palette = QPalette()
        palette.setColor(QPalette.Window,QColor("#EBF4DD"))
        self.setPalette(palette)

        layout = QVBoxLayout(self)

        self.main_label = QLabel("Download: 0.0 mbps/n\nUpload: 0.0 mpbs/n\nPing: 0.0 ms")
        self.main_label.setFont(QFont("San Francisco",24))
        self.update_label.connect(self.main_label.setText)
        layout.addWidget(self.main_label)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_test)
        self.start_btn.setFont(QFont("San Francisco",18))
        layout.addWidget(self.start_btn)

    def test_download(self):
        start = time.time()
        r = requests.get(f"{SERVER_URL}/download")
        _ = r.content
        end = time.time()

        size_bits = len(r.content) * 8
        speed = size_bits / (end - start) / 1_000_000
        return round(speed,2)

    def test_upload(self):
        data = b"x" * (5 * 1024 *1024)
        start = time.time()
        requests.post(f"{SERVER_URL}/upload",data=data)
        end = time.time()

        size_bits = len(data) * 8
        speed = size_bits / (end - start) / 1_000_000
        return round(speed,2)
    
    def test_ping(self):
        start = time.time()
        requests.get(f"{SERVER_URL}/ping")
        end = time.time()

        return round((end - start) * 1000,2)
    
    def start_test(self):
        self.main_label.setText("Testing...")
        thread = threading.Thread(target=self.run_test)
        thread.start()

    def run_test(self):
        try:
            download_speed = self.test_download()
            upload_speed = self.test_upload()
            ping = self.test_ping()

            result = (
                f"Download: {download_speed:.2f} Mbps/n\n"
                f"Upload: {upload_speed:.2f} Mbps/n\n"
                f"Ping: {ping} ms"
            )
            self.main_label.setText(result)
        except Exception as e:
            QMessageBox.warning(self,"Error",f"Error:\n{e}")
        
        

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SpeedTestApp()
    w.show()
    sys.exit(app.exec_())

