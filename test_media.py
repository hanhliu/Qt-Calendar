import sys
import os.path
# os.environ.setdefault('PYTHON_VLC_LIB_PATH', 'C:/Program Files/VideoLAN/VLC/libvlc.dll')
import vlc
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pydantic import AnyUrl
# from src.presentation.controller_main import MainController
from PySide6.QtCore import QObject
# from src.common.model.camera_model import CameraModel
# from src.common.widget.camera_state import CameraState
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtGui, QtCore
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()


class StreamCameraType:
    main_stream = "Main Stream"
    sub_stream = "Sub Stream"
    restream = "Restream"
    Rtmp = "RTMP"
    invalid = "Invalid"


class CameraState:
    paused = 'paused'
    started = 'started'
    stopped = 'stopped'
    opening = 'opening'


class MediaPlayerWrapper(QObject):
    """A wrapper for VLC Media Player functionalities"""
    camera_state_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.state = CameraState.stopped
        self.instance = vlc.Instance(
            '--avcodec-fast',  # Fast decoding
            '--avcodec-threads=4',  # Use 4 threads for decoding
            '--quiet',  # Reduce verbosity of logs
            '--no-osd',  # Disable on-screen display messages
            '--log-verbose=-1',  # Disable all logging
            '--avcodec-hurry-up',
            '--avcodec-workaround-bugs=1',
            '--avcodec-skiploopfilter=1'
        )
        self.media_list_player = self.instance.media_list_player_new()
        self.media_player = self.media_list_player.get_media_player()
        self.media_player.video_set_spu(10)
        self.media_player.audio_set_mute(True)
        self.media_player.video_set_mouse_input(False)
        self.media_player.video_set_key_input(False)
        self.media_path = None

        self.event_manager = self.media_player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.position_changed)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerOpening, self.media_player_opening)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self.media_player_started)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerPaused, self.media_player_paused)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.media_player_stopped)
        self.position_changed_callback = None

    def media_player_opening(self, event):
        logger.info(f"media_player_opening = {event.u.new_status}")
        self.state = CameraState.opening
        self.camera_state_signal.emit(self.state)

    def media_player_started(self, event):
        logger.info(f"media_player_started = {event.u.new_status}")
        self.state = CameraState.started
        self.camera_state_signal.emit(self.state)

    def media_player_paused(self, event):
        logger.info(f"media_player_paused = {event.u.new_status}")
        self.state = CameraState.paused
        self.camera_state_signal.emit(self.state)

    def media_player_stopped(self, event):
        logger.info(f"media_player_stopped = {event.u.new_status}")
        self.state = CameraState.stopped
        self.camera_state_signal.emit(self.state)

    def load_media(self, media_path, vlc_options=None):
        print(f'load_media: {media_path} - {vlc_options}')
        self.media_path = media_path

        # Check if media_path is a valid URL
        url = AnyUrl(media_path)

        # check scheme of url rtsp, http, https, ...
        if url.scheme == 'rtsp':
            # rtsp path need to be set to tcp for stable connection
            vlc_options = 'rtsp-tcp'

        if vlc_options:
            media = self.instance.media_new(media_path, vlc_options)
        else:
            media = self.instance.media_new(media_path)
        media_list = self.instance.media_list_new([media])
        self.media_list_player.set_media_list(media_list)
        # self.media_list_player.play_item_at_index(0)

    # get current url from media player
    def get_current_url(self):
        return self.media_path

    def get_xwindow(self):
        return self.media_player.get_xwindow()

    def play(self):
        print(f'play')
        self.media_list_player.play()

    def pause(self):
        self.media_list_player.pause()

    def stop(self):
        self.media_list_player.stop()

    def set_volume(self, volume):
        self.media_player.audio_set_volume(volume)

    def get_volume(self):
        return self.media_player.audio_get_volume()

    def set_position(self, position):
        self.media_player.set_position(position)

    def get_position(self):
        return self.media_player.get_position()

    def get_time(self):
        return self.media_player.get_time()

    def set_time(self, time):
        self.media_player.set_time(time)

    def get_duration(self):
        # get media
        media = self.media_player.get_media()
        # get duration
        duration = media.get_duration()
        return duration

    def is_playing(self):
        return self.media_player.is_playing()

    def get_length(self):
        return self.media_player.get_length()

    def set_window_id(self, videoframe):
        platform_setters = {
            'linux': lambda: self.media_player.set_xwindow(videoframe.winId()),
            'win32': lambda: self.media_player.set_hwnd(videoframe.winId()),
            'darwin': lambda: self.media_player.set_nsobject(int(videoframe.winId()))
        }
        platform_setters.get(sys.platform, lambda: None)()

    def position_changed(self, event):
        # self.callback(event)
        new_position = event.u.new_position
        # print(
        #     f'position_changed: {new_position} - get_position: {self.get_position()} - get_time: {self.get_time()} - get_duration: {self.get_duration()} - get_length: {self.get_length()}')
        if self.position_changed_callback:
            self.position_changed_callback(new_position)

    def set_speed(self, speed):
        self.media_player.set_rate(speed)

    def get_speed(self):
        return self.media_player.get_rate()

    def fetch_mpd_and_calculate_duration(self, url: str):
        try:
            result = subprocess.run(['curl', url], stdout=subprocess.PIPE)
            xml_content = result.stdout.decode('utf-8')
            root = ET.fromstring(xml_content)
            availability_start_time = root.attrib['availabilityStartTime']
            publish_time = root.attrib['publishTime']
            availability_start = datetime.fromisoformat(availability_start_time.replace("Z", "+00:00"))
            publish = datetime.fromisoformat(publish_time.replace("Z", "+00:00"))
            duration = publish - availability_start
            return duration.total_seconds() * 1000
        except Exception as e:
            print(f'Error: {e}')
            return -1




class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt"""

    def __init__(self, master=None):
        super().__init__(master)
        self.setWindowTitle("Media Player")

        self.media_player_wrapper = MediaPlayerWrapper()
        self.media_player_wrapper.camera_state_signal.connect(self.camera_state_signal)
        self.url_history = []
        self.is_slider_moving = False
        self.initUI()
        self.isPaused = False

        # Set the callback for position changes
        self.media_player_wrapper.position_changed_callback = self.on_position_changed

    def initUI(self):
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setMaximum(1000)
        self.positionslider.valueChanged.connect(self.valueChanged)
        self.positionslider.sliderPressed.connect(self.slider_pressed)
        self.positionslider.sliderReleased.connect(self.slider_released)
        self.positionslider.sliderMoved.connect(self.set_position)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)

        self.stopbutton = QtWidgets.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.stop)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.media_player_wrapper.get_volume())
        self.volumeslider.valueChanged.connect(self.set_volume)

        self.urllayout = QtWidgets.QHBoxLayout()
        self.urlinput = QtWidgets.QLineEdit(
            f'http://192.168.1.112:9000/video/videos/e2e365e9-73c7-4490-ac07-0e26d30549b1/2024_09_04/16_32/1725442339943/e2e365e9-73c7-4490-ac07-0e26d30549b1.mpd',
            self)
        # self.urlinput = QtWidgets.QLineEdit(
        #     f'D:\source_code\DAS-SN4225-SL_2024_04_03_1PM_23_16.mkv',
        #     self)
        self.urlinput.setPlaceholderText("Enter media URL here...")
        self.urlcompleter = QtWidgets.QCompleter(self.url_history, self)
        self.urlinput.setCompleter(self.urlcompleter)
        self.urllayout.addWidget(self.urlinput)

        self.vlcoptionslayout = QtWidgets.QHBoxLayout()
        self.vlcoptionsinput = QtWidgets.QLineEdit(self)
        self.vlcoptionsinput.setPlaceholderText("Enter VLC options here...")
        self.vlcoptionslayout.addWidget(self.vlcoptionsinput)

        self.loadbutton = QtWidgets.QPushButton("Load")
        self.urllayout.addWidget(self.loadbutton)
        self.loadbutton.clicked.connect(self.load_media)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addLayout(self.urllayout)
        self.vboxlayout.addLayout(self.vlcoptionslayout)
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open_action = QtGui.QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        exit_action = QtGui.QAction("&Exit", self)
        exit_action.triggered.connect(sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open_action)
        filemenu.addSeparator()
        filemenu.addAction(exit_action)

    def play_pause(self):
        if self.media_player_wrapper.is_playing():
            self.media_player_wrapper.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            self.media_player_wrapper.play()
            self.playbutton.setText("Pause")
            self.isPaused = False

    def stop(self):
        self.media_player_wrapper.stop()
        self.playbutton.setText("Play")

    def open_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if path:
            self.media_player_wrapper.load_media(path)
            self.media_player_wrapper.set_window_id(self.videoframe)
            self.play_pause()

    def load_media(self):
        url = self.urlinput.text()
        vlc_options = self.vlcoptionsinput.text()
        if url:
            if url not in self.url_history:
                self.url_history.append(url)
                self.urlcompleter.model().setStringList(self.url_history)
            self.media_player_wrapper.load_media(url, vlc_options)
            self.media_player_wrapper.set_window_id(self.videoframe)
            self.play_pause()

    def set_volume(self, volume):
        self.media_player_wrapper.set_volume(volume)

    def valueChanged(self, value):
        pass
        # logger.info(f"valueChanged = {value}")

    def slider_pressed(self):
        # print(f"slider_pressed  11111    self.media_player_wrapper.is_playing() = {self.media_player_wrapper.is_playing()}")
        self.is_slider_moving = True

    def slider_released(self):
        # logger.info("slider_released")
        position = self.positionslider.value() / 1000.0
        if position > 0.97:
            self.media_player_wrapper.stop()
            self.load_media()
            self.is_slider_moving = False
            return
        self.media_player_wrapper.set_position(position)
        # print(f"slider_released = {position}   22222222    self.media_player_wrapper.is_playing() = {self.media_player_wrapper.is_playing()}")
        self.is_slider_moving = False

    def set_position(self, position):
        # print(f"set_position = {self.is_slider_moving,position}")
        if self.is_slider_moving:
            convert_position = position / 1000.0
            # print(
            #     f'-----------------set_position: position: {position} -> convert_position: {convert_position} -----------------')
            self.media_player_wrapper.set_position(convert_position)
    def camera_state_signal(self,state):
        print(f'camera_state_signal: {state}')

    def on_position_changed(self, new_position):
        pass
        # print(f'on_position_changed: new_position: {self.is_slider_moving,new_position}')
        if not self.is_slider_moving:
            position = new_position * 1000.0000
            # print(f'on_position_changed: position: {position}')
            # print(f'on_position_changed: position: after convert int {int(position)}')
            self.positionslider.setValue(int(position))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    sys.exit(app.exec())
