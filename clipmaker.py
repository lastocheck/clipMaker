import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

class MyLineEdit(QLineEdit):

    mousePressedSignal = pyqtSignal(QPoint)

    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def mousePressEvent(self, event):
        self.mousePressedSignal.emit(event.pos())

class VideoPlayer(QWidget):

    def __init__(self, parent):
        print("super().__init__(parent)")
        super().__init__(parent)
        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        print("self.m_playButton = QPushButton()")
        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        print("self.m_positionSlider =QSlider(Qt.Horizontal)")
        self.positionSlider =QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        print("controlLayout = QHBoxLayout()")
        controlLayout = QHBoxLayout()
        #controlLayout.setMargin(0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        self.setLayout(layout)

        print("self.m_mediaPlayer.setVideoOutput(videoWidget)")
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)


    def setUrl(self, url):
        print("setUrl")
        self.errorLabel.setText("")
        if url.isLocalFile():
            print("url.isLocalFile()")
            self.setWindowFilePath(url.toLocalFile())
        else:
            print("else")
            self.setWindowFilePath('')
        #self.setWindowFilePath(url.isLocalFile() ? url.toLocalFile() : QString());
        self.mediaPlayer.setMedia(QMediaContent(url))
        print(url)

    def play(self):
        print("play")
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        print("mediaStateChanged")
        if state == QMediaPlayer.PlayingState:
            print("state == QMediaPlayer.PlayingState")
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            print("else")
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        print("positionChanged")
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        print("durationChanged")
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        print("setPosition")
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        print("handleError")
        #self.m_playButton.setEnabled(False)
        errorString = self.mediaPlayer.errorString()
        message = "Error: " + errorString
        self.errorLabel.setText(message)
        print(self.mediaPlayer.error())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.vbox = QVBoxLayout()

        self.fileUrl = None

        self.fileTextBox = MyLineEdit()
        self.fileTextBox.setMinimumWidth(600)
        self.fileTextBox.setReadOnly(True)
        self.fileTextBox.setPlaceholderText("Choose a file")
        self.fileTextBox.mousePressedSignal.connect(self.showFileDialog)
        self.vbox.addWidget(self.fileTextBox)

        self.player = VideoPlayer(self)
        self.vbox.addWidget(self.player)

        central = QWidget()
        central.setLayout(self.vbox)
        self.setCentralWidget(central)

        self.setWindowTitle("ClipMaker")
        self.show()

    def showFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a video file", QDir.homePath() + "/Videos",  "Video files (*.mp4 *.avi *.mkv)")
        fileInfo = QFileInfo(fileName)
        if fileInfo.exists():
            print("file exists")
        self.fileTextBox.setText(fileName)
        print("self.fileTextBox.setText(fileName[0])")
        if fileName[0] != '':
            print("self.fileName[0] != ''")
            self.fileUrl = QUrl.fromLocalFile(fileName)
            self.player.setUrl(self.fileUrl)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())