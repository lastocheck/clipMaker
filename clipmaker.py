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
        self.m_mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        print("self.m_playButton = QPushButton()")
        self.m_playButton = QPushButton()
        self.m_playButton.setEnabled(True)
        self.m_playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.m_playButton.clicked.connect(self.play)

        print("self.m_positionSlider =QSlider(Qt.Horizontal)")
        self.m_positionSlider =QSlider(Qt.Horizontal)
        self.m_positionSlider.setRange(0, 0)

        self.m_errorLabel = QLabel()
        self.m_errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        print("controlLayout = QHBoxLayout()")
        controlLayout = QHBoxLayout()
        #controlLayout.setMargin(0)
        controlLayout.addWidget(self.m_playButton)
        controlLayout.addWidget(self.m_positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.m_errorLabel)

        self.setLayout(layout)

        print("self.m_mediaPlayer.setVideoOutput(videoWidget)")
        self.m_mediaPlayer.setVideoOutput(videoWidget)
        self.m_mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.m_mediaPlayer.positionChanged.connect(self.positionChanged)
        self.m_mediaPlayer.durationChanged.connect(self.durationChanged)
        self.m_mediaPlayer.error.connect(self.handleError)


    def setUrl(self, url):
        print("setUrl")
        self.m_errorLabel.setText(QString())
        #self.setWindowFilePath(url.isLocalFile() ? url.toLocalFile() : QString());
        self.m_mediaPlayer.setMedia(url)

    def play():
        print("play")
        if self.m_mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.m_mediaPlayer.pause()
        else:
            self.m_mediaPlayer.play()

    def mediaStateChanged(state):
        print("mediaStateChanged")
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(position):
        print("positionChanged")
        self.m_positionSlider.setValue(position)

    def durationChanged(duration):
        print("durationChanged")
        self.m_positionSlider.setRange(0, duration)

    def setPosition(position):
        print("setPosition")
        self.m_mediaPlayer.setPosition(position)

    def handleError():
        print("handleError")
        self.m_playButton.setEnabled(False)
        errorString = self.m_mediaPlayer.errorString()
        message = "Error: " + errorString
        self.m_errorLabel.setText(message)


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

        self.player = VideoPlayer(self)
        self.vbox.addWidget(self.player)

        central = QWidget()
        central.setLayout(self.vbox)
        self.setCentralWidget(central)

        self.setWindowTitle("ClipMaker")
        self.show()

    def showFileDialog(self):
        fileName = QFileDialog.getOpenFileName(self, "Choose a video file", QDir.homePath() + "/Videos",  "Video files (*.mp4 *.avi *.mkv)")
        self.fileTextBox.setText(fileName[0])
        '''
        self.createVideoPlayer()

    def createVideoPlayer(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.vbox.addWidget(self.videoWidget)

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.vbox.addWidget(self.playButton)

        fileName = self.fileTextBox.text()
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            print("playing")
            self.mediaPlayer.play()
        '''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())