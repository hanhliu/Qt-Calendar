#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import os.path
import vlc
from PySide6 import QtWidgets, QtGui, QtCore

class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        # self._media_player = self.instance.media_player_new()
        self.init_player()

        self.createUI()
        self.isPaused = False
        self.is_click_progress = False
    
    def init_player(self):
        self._playlist_player = self.instance.media_list_player_new()
        self._playlist_player.set_playback_mode(vlc.PlaybackMode.repeat)

        self._media_player = self._playlist_player.get_media_player()

        self._media_player.audio_set_mute(True)
        self._media_player.video_set_mouse_input(False)
        self._media_player.video_set_key_input(False)

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtWidgets.QFrame()
        else:
            self.videoframe = QtWidgets.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.setPosition)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.PlayPause)

        self.stopbutton = QtWidgets.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.Stop)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self._media_player.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.volumeslider.valueChanged.connect(self.setVolume)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open = QtGui.QAction("&Open", self)
        open.triggered.connect(self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        exit.triggered.connect(sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        # self.timer.timeout.connect(self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self._media_player.is_playing():
            self._media_player.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self._media_player.play() == -1:
                self.OpenFile()
                return
            self._media_player.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self._media_player.stop()
        self.playbutton.setText("Play")

    def OpenFile(self):
        """Open a media file in a MediaPlayer
        """
        # # print(f"OpenFile - {filename}")
        # filename = None
        # if filename is None:
        #     print("filename is None")
        #     filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        #     print(filename)
        # if not filename:
        #     return
        # path = "http://192.168.1.145:9000/videos/7a851268-bd3b-4a43-b054-9a2245ff8c62/2024_07_24/14_39/1721806789916/7a851268-bd3b-4a43-b054-9a2245ff8c62.mpd"
        # path = "https://www.youtube.com/watch?v=k85mRPqvMbE"
        path = "/Users/hanhluu/Downloads/zeus.mp4"
        

        # create the media
        self._media_input_vlc = self.instance.media_new(path, 'rtsp-tcp')
        # self._media_input_vlc.add_options("--rtsp-tcp")

        playlist = self.instance.media_list_new()
        playlist.add_media(self._media_input_vlc)

        self._playlist_player.set_media_list(playlist)
        self._playlist_player.play_item_at_index(0)

        media_tracks = self._media_input_vlc.tracks_get()
        print(f'media_tracks: {media_tracks}')

        # put the media in the media player
        # self._media_player.set_media(self.media)

        # parse the metadata of the file
        # self.media.parse()

        # print(f'self.media.get_meta(0): {self.media.get_meta(0)}')

        
        # set the title of the track as window title
        self.setWindowTitle(f"{path}")
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in its own window)
        # this is platform-specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc; different platforms have different functions for this
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self._media_player.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self._media_player.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self._media_player.set_nsobject(int(self.videoframe.winId()))
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self._media_player.audio_set_volume(Volume)

    def setPosition(self, position):
        self.is_click_progress = True

        print(f'set to: {position/1000.0}')
        """Set the position
        """
        print(f'setPosition: self._media_player.get_position(): {self._media_player.get_position()}')
        print(f'setPosition: position / 1000.0: {(position / 1000.0)}')
        # setting the position to where the slider was dragged
        self._media_player.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise the results
        # (1000 should be enough)

        self.is_click_progress = False

    def updateUI(self):
        if self.is_click_progress:
            return
        """Updates the user interface"""
        # setting the slider to the desired position
        print(f'self._media_player.get_position(): {self._media_player.get_position()}')
        self.positionslider.setValue(int(self._media_player.get_position() * 1000))

        if not self._media_player.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button still shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())