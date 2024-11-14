import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel,
    QLineEdit, QTextEdit, QHBoxLayout, QApplication, QTableWidgetItem, QTableWidget
)

class Color:
    # dark theme
    primary_dark = "#5B5B9F"
    text_color_dark = "#F7F0F7"
    text_place_holder_dark = '#656475'
    text_disable_dark = '#656475'
    on_background_dark = '#2B2A3A'
    background_dark = '#181824'
    divider_dark = '#F7F0F7'  # use for border of QComboBox, QLineEdit focus
    divider_disable_dark = '#656475'  # use for border of QComboBox, QLineEdit not focus
    hover_primary_dark = ''

    # light theme
    primary_light = "#5B5B9F"
    text_color_light = "#717171"
    text_place_holder_light = "#CDCDCD"
    text_disable_light = '#CDCDCD'
    on_background_light = '#FBFBFB'
    background_light = '#D7D7D7'
    divider_light = '#717171'  # use for border of QComboBox, QLineEdit focus
    divider_disable_light = '#CDCDCD'  # use for border of QComboBox, QLineEdit not focus
    hover_primary_light = ''

    # common color for both theme
    primary_red = "#B5122E"
    primary_green = '#1CD1A1'
    white = "#FFFFFF"
    black = "#000000"
    error = '#FF0000'

    # default = "efefef"
    # primary_hover = "#3F3F87"
    # primary_pressed = "#3F3F87"
    # secondary = "#2B2A3A"
    # background = "#D7D7D7"
    # background_white = '#FBFBFB'
    # on_background = "#FBFBFB"
    # on_hover = "#656475"
    # on_hover_primary = "#3F3F87"
    # on_hover_secondary = "#656475"
    # on_hover_button = "#3F3F87"
    # hover_button_toolbar = "#656475"
    # background_item = "#363546"
    # background_item_off = "#2F2E3C"
    # # Text color
    # border_light = '#CDCDCD'
    # text_white = "#FFFFFF"
    # text_black = "#2B2A3A"
    # text_unselected = "#656475"
    # text_second_color = "#717171"
    # text_place_holder = "#CDCDCD"
    # text_disable = "#CDCDCD"
    # disable_color = "#CDCDCD"
    # text_on_primary = '#EEEEEE'
    # text_not_select = "#F7F0F7"
    # text_note = '#575757'
    # # border and stroke
    # border_line_edit = "#717171"
    # border_item = "#979797"
    # divider = "#CDCDCD"
    # border_line_edit_not_focus = "#CDCDCD"
    # # Button
    # button_second_background = "#656475"
    # button_primary_background = "#5B5B9F"
    # button_disable_background = "#242424"
    # # Menu
    # menu_title = "#A5A5A5"
    #
    # available = "#48DC6B"
    # unavailable = "#CC5051"
    # status_appear = "rgba(61, 173, 254, 1)"
    # status_checkin = "rgba(19, 172, 25, 1)"
    # status_checkout = "rgba(204, 80, 81, 1)"
    # text_camera_name = "rgba(255, 255, 255, 0.35)"
    # # divider = "rgba(42, 43, 50, 1)"
    # background_search_bar_event = "rgba(2, 2, 3, 0.45)"
    # text_search_bar_event = "rgba(255, 255, 255, 0.35)"
    # status_appear_dialog = "#41A0FA"
    # # event_number_color ='rgba(255, 145, 94, 1)'
    # event_number_color = "#FF915E"
    # button_color = "#3F3F87"
    # button_disable = "#DFE0E4"
    # border_button = "#5C687F"
    #
    # pulse_toggle_color = "#FFFFFF"
    # background_warning = "#CCCCD1"
    # transparent = "rgba(0, 0, 0, 0)"
    # button_upload = "#3388DC"
    # background_dialog = "#FFFFFF"
    # background_box = "#E99899"
    # background_box_hover = "#CC5051"
    # server_connected = "#1CD1A1"
    # widget_disable = "3A3A3A"

def get_darkModePalette():
    palette = QPalette()

    # Window and background
    palette.setColor(QPalette.ColorRole.Window, QColor(Color.background_dark))
    palette.setColor(QPalette.ColorRole.Base, QColor(Color.on_background_dark))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Color.divider_dark))

    # Text colors
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Color.text_color_dark))
    palette.setColor(QPalette.ColorRole.Text, QColor(Color.text_color_dark))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Color.text_color_dark))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(Color.text_place_holder_dark))
    # palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(Color.text_disable_dark))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(Color.text_disable_dark))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(Color.text_disable_dark))

    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor(Color.primary_dark))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Color.primary_dark))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Color.white))

    # Dividers and borders
    palette.setColor(QPalette.ColorRole.Light, QColor(Color.divider_dark))
    palette.setColor(QPalette.ColorRole.Mid, QColor(Color.divider_disable_dark))

    return palette
def get_lightModePalette():
    palette = QPalette()

    # Window and background
    palette.setColor(QPalette.ColorRole.Window, QColor(Color.background_light))
    palette.setColor(QPalette.ColorRole.Base, QColor(Color.on_background_light))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Color.divider_light))

    # Text colors
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Color.text_color_light))
    palette.setColor(QPalette.ColorRole.Text, QColor(Color.text_color_light))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Color.text_color_light))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(Color.text_place_holder_light))
    # palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(Color.text_disable_light))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(Color.text_disable_light))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(Color.text_disable_light))

    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor(Color.primary_light))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Color.primary_light))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Color.black))

    # Dividers and borders
    palette.setColor(QPalette.ColorRole.Light, QColor(Color.divider_light))
    palette.setColor(QPalette.ColorRole.Mid, QColor(Color.divider_disable_light))

    return palette

class ThemeSwitcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Initialize widgets
        self.init_widgets()

        # Set initial theme to light
        self.is_dark_theme = False
        self.apply_light_theme()

        # Set up the main window
        self.setWindowTitle("Theme Switcher App")
        self.setMinimumWidth(600)

    def init_widgets(self):
        # Theme switch button
        self.theme_switch_button = QPushButton("Switch to Dark Theme")
        self.theme_switch_button.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_switch_button)

        # ComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])

        self.layout.addWidget(QLabel("ComboBox:"))
        self.layout.addWidget(self.combo_box)

        # LineEdit
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter text here...")
        self.layout.addWidget(QLabel("LineEdit:"))
        self.layout.addWidget(self.line_edit)

        # TextEdit (multi-line text box)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter multiline text here...")
        self.layout.addWidget(QLabel("TextEdit:"))
        self.layout.addWidget(self.text_edit)

        # Buttons
        self.button1 = QPushButton("Button 1")
        self.button1.setIcon(QIcon('assets/close.svg'))
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton()
        self.button4.setIcon(QIcon('assets/normal_window.svg'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addWidget(self.button4)
        self.layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setRowCount(4)  # Set number of rows
        self.table.setColumnCount(3)  # Set number of columns
        self.table.setHorizontalHeaderLabels(["Name", "Age", "City"])

        # Add data to the table
        data = [
            ("John Doe", "28", "New York"),
            ("Jane Smith", "34", "London"),
            ("Mike Johnson", "45", "Sydney"),
            ("Anna Lee", "23", "Tokyo"),
        ]

        for row, (name, age, city) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(age))
            self.table.setItem(row, 2, QTableWidgetItem(city))

        # Connect cell click signal to a custom slot
        self.table.cellClicked.connect(self.cell_clicked)
        self.layout.addWidget(self.table)

    def cell_clicked(self, row, column):
        # Get the clicked cell's content
        item = self.table.item(row, column)
        if item is not None:
            print(f"Clicked on cell ({row}, {column}): {item.text()}")

    def toggle_theme(self):
        # Switch between light and dark theme
        if self.is_dark_theme:
            self.apply_light_theme()
            self.theme_switch_button.setText("Switch to Dark Theme")
        else:
            self.apply_dark_theme()
            self.theme_switch_button.setText("Switch to Light Theme")
        self.is_dark_theme = not self.is_dark_theme

    def apply_light_theme(self):
        app.setPalette(get_lightModePalette())

    def apply_dark_theme(self):
        app.setPalette(get_darkModePalette())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ThemeSwitcherApp()

    window.show()
    sys.exit(app.exec())

