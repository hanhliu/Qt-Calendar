import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_video)
        self.layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_video)
        self.layout.addWidget(self.stop_button)

        self.video_url = QUrl.fromLocalFile("/Users/hanhluu/Documents/Project/Qt/calendar_project/assets/chairandbeach.mp4")  # Replace with your video file path
        self.media_content = QMediaContent(self.video_url)

    def play_video(self):
        self.media_player.setMedia(self.media_content)
        self.media_player.play()

    def stop_video(self):
        self.media_player.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VideoPlayerApp()
    main_window.show()
    sys.exit(app.exec_())
