import os
import sys

import pygame
from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton

from language_switcher import LanguageSwitcher


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.current_locale = QLocale.system().name()
        self.load_ui()

    def load_ui(self):
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        label = QLabel("Init QMain Window")
        self.central_layout.addWidget(label)

        # create label
        self.mylabel = QLabel(self.tr("Qt Init Widget"))
        # center
        self.mylabel.setAlignment(Qt.AlignCenter)

        pygame.mixer.init()
        self.audio_file = "/assets/notifi.mp3"

        self.label_1 = QLabel(self.tr("This is a QLabel 1"))
        self.button_1 = QPushButton(self.tr("Press me 1"))
        self.button_2 = QPushButton(self.tr("Press me 2"))
        self.button_3 = QPushButton(self.tr("Press me 3"))
        self.button_change_language = QPushButton(self.tr("Change Language"))
        self.button_change_language.clicked.connect(self.change_language)

        self.central_layout.addWidget(self.mylabel)
        self.central_layout.addWidget(self.label_1)
        self.central_layout.addWidget(self.button_1)
        self.central_layout.addWidget(self.button_2)
        self.central_layout.addWidget(self.button_3)
        self.central_layout.addWidget(self.button_change_language)

        self.setCentralWidget(self.central_widget)

    def change_language(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.set_volume(1.0)  # Set volume
        pygame.mixer.music.play(-1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the default language
    default_locale = QLocale.system().name()

    print("HanhLT: default_locale   ", default_locale)

    # Create and install the translator
    translator = QTranslator()
    translator.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/src/translations/test_" +default_locale+".qm")
    app.installTranslator(translator)

    window = MainWindow()
    # # Create the language switcher instance
    # language_switcher = LanguageSwitcher()
    #
    # # Define a slot to update the translations dynamically
    # def updateTranslations(locale):
    #     translator.load("/Users/hanhluu/Documents/Project/Qt/calendar_project/src/translations/test_" + locale+".qm")
    #     app.installTranslator(translator)
    #     window.update()
    #
    # # Connect the language switch signal to the updateTranslations slot
    # language_switcher.languageChanged.connect(updateTranslations)
    # language_switcher.switchLanguage("vi_VN")

    window.show()
    sys.exit(app.exec())


