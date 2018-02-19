import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyLineEdit(QLineEdit):

    mousePressedSignal = pyqtSignal(QPoint)

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def mousePressEvent(self, event):
        self.mousePressedSignal.emit(event.pos())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.vbox = QVBoxLayout()

        self.fileTextBox = MyLineEdit()
        self.fileTextBox.setMinimumWidth(600)
        self.fileTextBox.setReadOnly(True)
        self.fileTextBox.setPlaceholderText("Choose a file")
        self.fileTextBox.mousePressedSignal.connect(self.showFileDialog)
        self.vbox.addWidget(self.fileTextBox)

        central = QWidget()
        central.setLayout(self.vbox)
        self.setCentralWidget(central)

        self.setWindowTitle("ClipMaker")
        self.show()

    def showFileDialog(self):
        fileName = QFileDialog.getOpenFileName(self, "Choose a video file", QDir.homePath() + "/Videos",  "Video files (*.mp4 *.avi *.mkv)")
        self.fileTextBox.setText(fileName[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())