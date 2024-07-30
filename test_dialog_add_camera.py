import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QGuiApplication, QAction, QStandardItemModel, QStandardItem, QPainter, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHeaderView, QCheckBox, QStyleOptionButton, QStyle, QHBoxLayout, QAbstractItemView, QPushButton, QLabel, QDialog, \
    QLineEdit, QItemDelegate, QComboBox, QStackedWidget, QFrame, QTextEdit, QTableView, QSizePolicy


class NewAddCameraDialog(QDialog):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        # logger.info("Init AddCameraGroupDialog")
        screen = QGuiApplication.primaryScreen()
        self.desktop_screen_size = screen.availableGeometry()
        # self.controller = MainController()
        # self.setWindowTitle(self.tr('Add Camera Group'))
        self.setMinimumWidth(self.desktop_screen_size.width() * 0.5)
        self.setModal(False)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # QApplication.instance().installEventFilter(self)
        self.style_sheet_active_button = '''
                    QPushButton{
                        background-color: #1C2039;
                        padding: 4px;
                        color: white;
                        border: None;
                        border-top-left-radius: 4px;  /* Set top-left border radius */
                        border-top-right-radius: 4px;
                    }
                '''
        self.style_sheet_inactive_button = '''
                    QPushButton{
                        background-color: transparent;
                        padding: 4px;
                        color: black;
                        border: None;
                    }
                '''
        self.create_title_bar()
        self.create_content_widget()
        self.load_ui()
        self.update_style()

        self.resize(self.desktop_screen_size.width() * 0.5,
                    self.desktop_screen_size.height() * 0.6)

    def load_ui(self):
        self.layout_dialog = QVBoxLayout()
        self.layout_dialog.setContentsMargins(0, 0, 0, 0)
        self.layout_dialog.setSpacing(0)

        self.save_cancel = QWidget()
        self.save_cancel.setStyleSheet(
            "background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        self.layout_save_cancel = QHBoxLayout()
        self.layout_save_cancel.setContentsMargins(0, 0, 0, 0)
        self.btn_save = QPushButton(self.tr("Create"))
        self.btn_save.setFixedSize(120, 32)
        # self.btn_save.setStyleSheet(Style.StyleSheet.button_style1)
        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_cancel = QPushButton(self.tr("Cancel"))
        # self.btn_cancel.setStyleSheet(Style.StyleSheet.button_style2)
        self.btn_cancel.setFixedSize(120, 32)
        self.btn_cancel.clicked.connect(self.cancel_clicked)
        self.layout_save_cancel.addWidget(QWidget())
        self.layout_save_cancel.addWidget(self.btn_save)
        self.layout_save_cancel.addWidget(self.btn_cancel)
        self.layout_save_cancel.addWidget(QWidget())
        self.save_cancel.setLayout(self.layout_save_cancel)

        self.layout_dialog.setAlignment(self.save_cancel, Qt.AlignBottom)
        self.layout_dialog.addWidget(self.title_bar_widget, 1)
        self.layout_dialog.addWidget(self.content_widget, 90)
        self.layout_dialog.addWidget(self.save_cancel, 1)
        self.setLayout(self.layout_dialog)

    def create_content_widget(self):
        self.create_layout_server()
        self.create_layout_main_content()
        self.content_widget = QWidget()
        self.layout_content_widget = QVBoxLayout()
        self.layout_content_widget.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_content_widget.addLayout(self.layout_server)
        self.layout_content_widget.addLayout(self.layout_tab_content)
        self.content_widget.setLayout(self.layout_content_widget)

    def create_layout_server(self):
        self.layout_server = QHBoxLayout()
        self.layout_server.setSpacing(4)
        self.layout_server.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_to_server = QLabel(self.tr('Server:'))
        self.combo_box_server = QComboBox()
        self.combo_box_server.setFixedSize(300, 28)
        # Create a QStandardItemModel
        model = QStandardItemModel()
        # Create items with icons and text
        item1 = QStandardItem(self.tr("192.168.1.123"))
        item2 = QStandardItem(self.tr("123.24.1.24"))
        item3 = QStandardItem(self.tr("192.168.10.1"))
        # Add items to the model
        model.appendRow(item1)
        model.appendRow(item2)
        model.appendRow(item3)
        # Set the model for the ComboBox
        self.combo_box_server.setModel(model)
        # Create a delegate to display icons and text
        delegate = QItemDelegate(self.combo_box_server)
        self.combo_box_server.setItemDelegate(delegate)
        # Set a style sheet for the ComboBox
        self.combo_box_server.setStyleSheet(f'''
                QComboBox {{ 
                    background-color: #EFEFEF; 
                    border: None;
                    border-radius: 4px;
                }}
                QComboBox::drop-down {{
                     background-color: #EFEFEF;
                     border: None;
                     border-radius: 4px;
                 }}
                QComboBox::down-arrow {{ 
                    image: url(':assets/sort-down.png'); 
                }}
            ''')
        self.layout_server.addWidget(self.label_to_server)
        self.layout_server.addWidget(self.combo_box_server)

    def create_layout_main_content(self):
        self.create_widget_known_address()
        self.create_widget_subnet_scan()

        self.layout_tab_content = QVBoxLayout()
        self.layout_tab_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_tab_content.setContentsMargins(0, 0, 0, 0)
        self.layout_tab_content.setSpacing(0)

        self.widget_button_top = QWidget()
        self.layout_button_top = QHBoxLayout(self.widget_button_top)
        self.layout_button_top.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.layout_button_top.setSpacing(0)
        self.layout_button_top.setContentsMargins(0, 0, 0, 0)
        divider1 = self.create_divider()
        divider2 = self.create_divider()

        self.button_known_address = QPushButton('Known Address')
        self.button_known_address.setFixedHeight(30)
        self.button_known_address.setStyleSheet(self.style_sheet_active_button)
        self.button_known_address.clicked.connect(self.btn_known_address_clicked)
        self.button_subnet_scan = QPushButton('Subnet Scan')
        self.button_subnet_scan.setFixedHeight(30)
        self.button_subnet_scan.setStyleSheet(self.style_sheet_inactive_button)
        self.button_subnet_scan.clicked.connect(self.btn_subnet_scan_clicked)
        self.layout_button_top.addWidget(divider1)
        self.layout_button_top.addWidget(self.button_known_address)
        self.layout_button_top.addWidget(self.button_subnet_scan)
        self.layout_button_top.addWidget(divider2)

        self.stacked_widget_main = QStackedWidget()
        self.stacked_widget_main.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget_main.addWidget(self.widget_content_known_address)
        self.stacked_widget_main.addWidget(self.widget_subnet_scan)

        self.layout_tab_content.addWidget(self.widget_button_top)
        self.layout_tab_content.addWidget(self.stacked_widget_main)

    def create_widget_known_address(self):
        self.widget_content_known_address = QWidget()
        self.widget_content_known_address.setStyleSheet('background-color: #EFEFEF')
        self.layout_content_known_address = QVBoxLayout(self.widget_content_known_address)
        self.layout_content_known_address.setContentsMargins(20, 0, 20, 0)
        self.layout_content_known_address.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_content_known_address.setSpacing(10)

        self.widget_input_to_search = QWidget()
        self.layout_input_to_search = QHBoxLayout(self.widget_input_to_search)
        self.layout_input_to_search.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_input_to_search.setContentsMargins(0, 20, 0, 0)

        label_address = QLabel(self.tr('Address:'))
        label_address.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_address.setFixedHeight(32)
        label_port = QLabel(self.tr('Port:'))
        label_port.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_port.setFixedHeight(32)
        layout_address_and_port = QVBoxLayout()
        layout_address_and_port.setContentsMargins(0, 0, 0, 0)
        layout_address_and_port.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_address_and_port.addWidget(label_address)
        layout_address_and_port.addWidget(label_port)

        text_edit_known_address = self.text_edit_with_style('IP/Hostname/RTSP/UDP Link')
        widget_port = self.widget_ports()
        layout_IP_and_PORT = QVBoxLayout()
        layout_IP_and_PORT.setContentsMargins(0, 0, 0, 0)
        layout_IP_and_PORT.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_IP_and_PORT.addWidget(text_edit_known_address)
        layout_IP_and_PORT.addWidget(widget_port)

        label_login = QLabel(self.tr('Login:'))
        label_login.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_login.setFixedHeight(32)
        label_password = QLabel(self.tr('Password:'))
        label_password.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_password.setFixedHeight(32)
        layout_login_and_password = QVBoxLayout()
        layout_login_and_password.setContentsMargins(0, 0, 0, 0)
        layout_login_and_password.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_login_and_password.addWidget(label_login)
        layout_login_and_password.addWidget(label_password)

        text_edit_login = self.text_edit_with_style(self.tr('Username'))
        text_edit_password = self.text_edit_with_style(self.tr('Password'))
        layout_text_edit_login_password = QVBoxLayout()
        layout_text_edit_login_password.setContentsMargins(0, 0, 0, 0)
        layout_text_edit_login_password.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_text_edit_login_password.addWidget(text_edit_login)
        layout_text_edit_login_password.addWidget(text_edit_password)

        self.layout_input_to_search.addLayout(layout_address_and_port, 10)
        self.layout_input_to_search.addLayout(layout_IP_and_PORT, 50)
        self.layout_input_to_search.addLayout(layout_login_and_password, 10)
        self.layout_input_to_search.addLayout(layout_text_edit_login_password, 30)

        widget_btn_search = QWidget()
        self.button_search = QPushButton('Search')
        self.button_search.setFixedSize(70, 30)
        self.button_search.setStyleSheet('''
            QPushButton{
                background-color: #B5122E;
                padding: 4px;
                color: white;
                border: None;
                border-radius: 4px;
            }
        ''')
        layout_btn_search = QVBoxLayout(widget_btn_search)
        layout_btn_search.setContentsMargins(0, 0, 0, 0)
        layout_btn_search.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_btn_search.addWidget(self.button_search)
        horizontal_divider = self.create_divider(self.desktop_screen_size.width() * 0.465, 2, QFrame.Shape.HLine)

        widget_table_result_search = QWidget()
        layout_table_result_search = QVBoxLayout(widget_table_result_search)
        layout_table_result_search.setAlignment(Qt.AlignmentFlag.AlignTop |Qt.AlignmentFlag.AlignLeft)
        layout_table_result_search.setContentsMargins(0, 0, 0, 0)
        list_horizontal_header = ["", "Brand", "Model", "Address", "Status"]
        widget_checkbox = QWidget()
        layout_checkbox = QVBoxLayout()
        layout_checkbox.setContentsMargins(0, 0, 0, 0)
        layout_checkbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox = QCheckBox()
        # checkbox.stateChanged.connect(self.check_all)
        checkbox.setTristate(False)
        layout_checkbox.addWidget(checkbox)
        widget_checkbox.setLayout(layout_checkbox)
        list_widget_for_header = {0: widget_checkbox}

        self.model_table_known_address = QStandardItemModel(4, 5)
        self.table_result_known_address = TableResultCamera(horizontal_label_list=list_horizontal_header,
                                                            list_widget_to_header=list_widget_for_header,
                                                            model_for_table=self.model_table_known_address)
        self.table_result_known_address.table.setColumnWidth(0, 44)
        self.table_result_known_address.table.setColumnWidth(1, 170)
        self.table_result_known_address.table.setColumnWidth(2, 180)
        self.table_result_known_address.table.setColumnWidth(3, 400)
        self.table_result_known_address.table.setColumnWidth(4, 90)
        self.table_result_known_address.table.verticalHeader().setVisible(False)
        self.table_result_known_address.table.verticalHeader().setDefaultSectionSize(38)
        self.table_result_known_address.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_result_known_address.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_result_known_address.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_result_known_address.table.setFocusPolicy(Qt.NoFocus)
        self.table_result_known_address.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_result_known_address.table.setShowGrid(False)
        # Add checkboxes to the first column and text to the other columns
        for row in range(6):
            checkbox_item = QStandardItem()
            checkbox_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_item.setCheckable(True)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.model_table_known_address.setItem(row, 0, checkbox_item)
            item = QStandardItem(f"Item {row + 1}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model_table_known_address.setItem(row, 1, item)
            self.model_table_known_address.setItem(row, 2, item)
            self.model_table_known_address.setItem(row, 3, item)
            self.model_table_known_address.setItem(row, 4, item)

        total_device_in_known_address = self.ui_widget_group_with_total_device()
        layout_table_result_search.addWidget(self.table_result_known_address, 90)
        layout_table_result_search.addWidget(total_device_in_known_address)

        self.layout_content_known_address.addWidget(self.widget_input_to_search)
        self.layout_content_known_address.addWidget(widget_btn_search)
        self.layout_content_known_address.addWidget(horizontal_divider)

        widget_no_data = QWidget()
        layout_no_data = QVBoxLayout(widget_no_data)

        widget_image_init = QWidget()
        layout_image_init = QVBoxLayout(widget_image_init)

        self.stacked_widget_result_search = QStackedWidget()
        self.stacked_widget_result_search.addWidget(widget_table_result_search)
        self.stacked_widget_result_search.addWidget(widget_no_data)
        self.stacked_widget_result_search.addWidget(widget_image_init)

        self.layout_content_known_address.addWidget(self.stacked_widget_result_search, 90)

    def create_widget_subnet_scan(self):
        self.widget_subnet_scan = QWidget()
        self.widget_subnet_scan.setStyleSheet('background-color: #EFEFEF')
        self.layout_content_subnet_scan = QVBoxLayout(self.widget_subnet_scan)
        self.layout_content_subnet_scan.setContentsMargins(20, 0, 20, 0)
        self.layout_content_subnet_scan.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_content_subnet_scan.setSpacing(10)

        self.widget_input_to_scan = QWidget()
        self.layout_input_to_scan = QHBoxLayout(self.widget_input_to_scan)
        self.layout_input_to_scan.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_input_to_scan.setContentsMargins(0, 20, 0, 0)

        star_ip_address = QLabel(self.tr('Start IP:'))
        star_ip_address.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        star_ip_address.setFixedHeight(32)
        end_ip_address = QLabel(self.tr('End IP:'))
        end_ip_address.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        end_ip_address.setFixedHeight(32)
        label_port = QLabel(self.tr('Port:'))
        label_port.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_port.setFixedHeight(32)
        layout_address_and_port = QVBoxLayout()
        layout_address_and_port.setContentsMargins(0, 0, 0, 0)
        layout_address_and_port.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_address_and_port.addWidget(star_ip_address)
        layout_address_and_port.addWidget(end_ip_address)
        layout_address_and_port.addWidget(label_port)

        text_edit_start_ip = self.text_edit_with_style('0.0.0.0')
        text_edit_end_ip = self.text_edit_with_style('0.0.0.255')
        widget_port = self.widget_ports()
        layout_IP_and_PORT = QVBoxLayout()
        layout_IP_and_PORT.setContentsMargins(0, 0, 0, 0)
        layout_IP_and_PORT.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_IP_and_PORT.addWidget(text_edit_start_ip)
        layout_IP_and_PORT.addWidget(text_edit_end_ip)
        layout_IP_and_PORT.addWidget(widget_port)

        label_login = QLabel(self.tr('Login:'))
        label_login.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_login.setFixedHeight(32)
        label_password = QLabel(self.tr('Password:'))
        label_password.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        label_password.setFixedHeight(32)
        layout_login_and_password = QVBoxLayout()
        layout_login_and_password.setContentsMargins(0, 0, 0, 0)
        layout_login_and_password.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_login_and_password.addWidget(label_login)
        layout_login_and_password.addWidget(label_password)

        text_edit_login = self.text_edit_with_style(self.tr('Username'))
        text_edit_password = self.text_edit_with_style(self.tr('Password'))
        layout_text_edit_login_password = QVBoxLayout()
        layout_text_edit_login_password.setContentsMargins(0, 0, 0, 0)
        layout_text_edit_login_password.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_text_edit_login_password.addWidget(text_edit_login)
        layout_text_edit_login_password.addWidget(text_edit_password)

        self.layout_input_to_scan.addLayout(layout_address_and_port, 10)
        self.layout_input_to_scan.addLayout(layout_IP_and_PORT, 50)
        self.layout_input_to_scan.addLayout(layout_login_and_password, 10)
        self.layout_input_to_scan.addLayout(layout_text_edit_login_password, 30)

        widget_btn_search = QWidget()
        self.button_scan = QPushButton('Scan')
        self.button_scan.setFixedSize(70, 30)
        self.button_scan.setStyleSheet('''
                    QPushButton{
                        background-color: #B5122E;
                        padding: 4px;
                        color: white;
                        border: None;
                        border-radius: 4px;
                    }
                ''')
        layout_btn_search = QVBoxLayout(widget_btn_search)
        layout_btn_search.setContentsMargins(0, 0, 0, 0)
        layout_btn_search.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_btn_search.addWidget(self.button_scan)
        horizontal_divider = self.create_divider(self.desktop_screen_size.width() * 0.465, 2, QFrame.Shape.HLine)

        widget_table_result_scan = QWidget()
        layout_table_result_scan = QVBoxLayout(widget_table_result_scan)
        layout_table_result_scan.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_table_result_scan.setContentsMargins(0, 0, 0, 0)
        list_horizontal_header = ["", "Brand", "Model", "Address", "Status"]
        widget_checkbox = QWidget()
        layout_checkbox = QVBoxLayout()
        layout_checkbox.setContentsMargins(0, 0, 0, 0)
        layout_checkbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox = QCheckBox()
        # checkbox.stateChanged.connect(self.check_all)
        checkbox.setTristate(False)
        layout_checkbox.addWidget(checkbox)
        widget_checkbox.setLayout(layout_checkbox)
        list_widget_for_header = {0: widget_checkbox}

        self.model_table_scan = QStandardItemModel(4, 5)
        self.table_result_scan = TableResultCamera(horizontal_label_list=list_horizontal_header,
                                                            list_widget_to_header=list_widget_for_header,
                                                            model_for_table=self.model_table_scan)
        self.table_result_scan.table.setColumnWidth(0, 44)
        self.table_result_scan.table.setColumnWidth(1, 170)
        self.table_result_scan.table.setColumnWidth(2, 180)
        self.table_result_scan.table.setColumnWidth(3, 400)
        self.table_result_scan.table.setColumnWidth(4, 90)
        self.table_result_scan.table.verticalHeader().setVisible(False)
        self.table_result_scan.table.verticalHeader().setDefaultSectionSize(38)
        self.table_result_scan.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_result_scan.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_result_scan.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_result_scan.table.setFocusPolicy(Qt.NoFocus)
        self.table_result_scan.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_result_scan.table.setShowGrid(False)
        # Add checkboxes to the first column and text to the other columns
        for row in range(6):
            checkbox_item = QStandardItem()
            checkbox_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_item.setCheckable(True)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.model_table_scan.setItem(row, 0, checkbox_item)
            item = QStandardItem(f"Item {row + 1}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model_table_scan.setItem(row, 1, item)
            self.model_table_scan.setItem(row, 2, item)
            self.model_table_scan.setItem(row, 3, item)
            self.model_table_scan.setItem(row, 4, item)

        total_device_in_scan = self.ui_widget_group_with_total_device()
        layout_table_result_scan.addWidget(self.table_result_scan, 90)
        layout_table_result_scan.addWidget(total_device_in_scan)

        self.layout_content_subnet_scan.addWidget(self.widget_input_to_scan)
        self.layout_content_subnet_scan.addWidget(widget_btn_search)
        self.layout_content_subnet_scan.addWidget(horizontal_divider)

        widget_no_data = QWidget()
        layout_no_data = QVBoxLayout(widget_no_data)

        widget_image_init = QWidget()
        layout_image_init = QVBoxLayout(widget_image_init)

        self.stacked_widget_result_search = QStackedWidget()
        self.stacked_widget_result_search.addWidget(widget_table_result_scan)
        self.stacked_widget_result_search.addWidget(widget_no_data)
        self.stacked_widget_result_search.addWidget(widget_image_init)

        self.layout_content_subnet_scan.addWidget(self.stacked_widget_result_search)

    def create_title_bar(self):
        # layout
        self.title_bar_widget = QWidget()
        self.title_bar_widget.setObjectName("title_bar")
        # set background Style.Color.primary
        self.title_bar_widget.setStyleSheet(
            f"background-color: #B5122E; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        self.title_bar_layout = QHBoxLayout()
        # event name
        self.title_name_label = QLabel(self.tr("ADD CAMERAS"))
        self.title_name_label.setStyleSheet(
            f"color: #FFFFFF; font-size: 14px")
        close_icon = QIcon('assets/close.svg')
        self.close_button = QPushButton(close_icon, "")
        self.close_button.setIconSize(QSize(30, 30))
        self.close_button.setFixedSize(30, 30)
        # self.close_button.setStyleSheet(Style.StyleSheet.button_style14)
        self.close_button.clicked.connect(self.close)
        # add widget
        self.title_bar_layout.addWidget(self.title_name_label, 90)
        self.title_bar_layout.addWidget(self.close_button, 10)
        self.title_bar_widget.setLayout(self.title_bar_layout)

    def create_divider(self, width=1, height=12, shape=QFrame.Shape.VLine):
        divider = QFrame()
        divider.setFixedSize(width, height)
        divider.setFrameShape(shape)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #8D9DB1;")
        return divider

    def widget_text_and_line_edit(self, title, place_holder_text):
        widget_container = QWidget()
        layout_container = QHBoxLayout()
        layout_container.setContentsMargins(0, 0, 0, 0)
        layout_container.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_container.setSpacing(10)
        label_title = QLabel(title)
        text_edit = QTextEdit()
        text_edit.setFixedHeight(32)
        text_edit.setPlaceholderText(place_holder_text)
        layout_container.addWidget(label_title, 20)
        layout_container.addWidget(text_edit, 80)
        widget_container.setLayout(layout_container)
        return widget_container

    def text_edit_with_style(self, place_holder_text):
        text_edit = QLineEdit()

        text_edit.setStyleSheet('''
            QLineEdit{
                padding: 2px;
                background-color: white;
                color: black;
                border: None;
                border-radius: 4px;
            }
        ''')
        text_edit.setFixedHeight(28)
        text_edit.setPlaceholderText(place_holder_text)
        return text_edit

    def ui_widget_group_with_total_device(self):
        label_total_device = QLabel(self.tr('6 Devices'))
        label_total_device.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_group_with_combobox = QHBoxLayout()
        layout_group_with_combobox.setContentsMargins(0, 0, 0, 0)
        layout_group_with_combobox.setSpacing(10)
        layout_group_with_combobox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_group = QLabel(self.tr('Add to Groups:'))
        combo_box_group = QComboBox()
        combo_box_group.setFixedSize(200, 28)
        # Create a QStandardItemModel
        model = QStandardItemModel()
        # Create items with icons and text
        item1 = QStandardItem('Group 1')
        item2 = QStandardItem('Group 2')
        item3 = QStandardItem('Group 3')
        # Add items to the model
        model.appendRow(item1)
        model.appendRow(item2)
        model.appendRow(item3)
        # Set the model for the ComboBox
        combo_box_group.setModel(model)
        # Create a delegate to display icons and text
        delegate = QItemDelegate(self.combo_box_server)
        combo_box_group.setItemDelegate(delegate)
        # Set a style sheet for the ComboBox
        combo_box_group.setStyleSheet(f'''
            QComboBox {{ 
                background-color: white; 
                border: None;
                border-radius: 4px;
            }}
            QComboBox::drop-down {{
                 background-color: white;
                 border: None;
                 border-radius: 4px;
             }}
            QComboBox::down-arrow {{ 
                image: url(':assets/sort-down.png'); 
            }}
        ''')
        layout_group_with_combobox.addWidget(label_group)
        layout_group_with_combobox.addWidget(combo_box_group)
        widget_group_with_total_device = QWidget()
        layout_group_with_total_device = QVBoxLayout(widget_group_with_total_device)
        layout_group_with_total_device.setContentsMargins(0, 0, 0, 4)
        layout_group_with_total_device.setSpacing(8)
        layout_group_with_total_device.addWidget(label_total_device)
        layout_group_with_total_device.addLayout(layout_group_with_combobox)
        return widget_group_with_total_device

    def widget_ports(self):
        widget_port = QWidget()
        layout_port = QHBoxLayout()
        layout_port.setContentsMargins(0, 0, 0, 0)
        layout_port.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout_port.setSpacing(10)
        combo_box_port = QComboBox()
        combo_box_port.setFixedSize(200, 28)
        # Create a QStandardItemModel
        model = QStandardItemModel()
        # Create items with icons and text
        item1 = QStandardItem('80')
        item2 = QStandardItem('80')
        item3 = QStandardItem('80')
        # Add items to the model
        model.appendRow(item1)
        model.appendRow(item2)
        model.appendRow(item3)
        # Set the model for the ComboBox
        combo_box_port.setModel(model)
        # Create a delegate to display icons and text
        delegate = QItemDelegate(self.combo_box_server)
        combo_box_port.setItemDelegate(delegate)
        # Set a style sheet for the ComboBox
        combo_box_port.setStyleSheet(f'''
            QComboBox {{ 
                background-color: white; 
                border: None;
                border-radius: 4px;
            }}
            QComboBox::drop-down {{
                 background-color: white;
                 border: None;
                border-radius: 4px;
             }}
            QComboBox::down-arrow {{ 
                image: url(':assets/sort-down.png'); 
            }}
        ''')

        checkbox_default = QCheckBox(self.tr('Default'))
        layout_port.addWidget(combo_box_port)
        layout_port.addWidget(checkbox_default)
        widget_port.setLayout(layout_port)
        return widget_port

    def save_clicked(self):
        pass

    def cancel_clicked(self):
        self.close()

    def btn_known_address_clicked(self):
        self.stacked_widget_main.setCurrentIndex(0)
        self.button_known_address.setStyleSheet(self.style_sheet_active_button)
        self.button_subnet_scan.setStyleSheet(self.style_sheet_inactive_button)

    def btn_subnet_scan_clicked(self):
        self.stacked_widget_main.setCurrentIndex(1)
        self.button_subnet_scan.setStyleSheet(self.style_sheet_active_button)
        self.button_known_address.setStyleSheet(self.style_sheet_inactive_button)

    def click_server_line_edit(self, event):
        print(f"HanhLT: click_server_line_edit = {event}")

    def click_to_select_server(self):
        print('click_to_select_server')

    def update_style(self):
        self.setStyleSheet(
            f'''
                    QWidget {{
                        background-color: white;
                        color: #1C2039;
                    }}
                    '''
        )

class TableResultCamera(QWidget):
    def __init__(self, horizontal_label_list=None, model_for_table=None, list_widget_to_header: dict[int, QWidget] = None):
        super().__init__()
        self.horizontal_label_list = horizontal_label_list
        self.model_for_table = model_for_table
        self.list_widget_to_header = list_widget_to_header
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.load_ui()

    def load_ui(self):
        self.table = TableViewBase()
        self.table.setStyleSheet("""
                    QTableView {
                        border: None;
                        gridline-color: #dcdcdc;
                        background-color: transparent;
                    }
                    QHeaderView::section {
                        background-color: transparent;
                        padding: 4px;
                        border: None;
                        font-weight: bold;
                        font-size: 14px;
                    }
                    QTableView::item {
                        padding: 5px;
                    }
                    QTableView::item:selected {
                        background-color: #a0a0ff;
                        color: #ffffff;
                    }
                """)
        self.model_for_table.setHorizontalHeaderLabels(self.horizontal_label_list)
        # Set the model for the table view
        self.table.setModel(self.model_for_table)

        # Set the custom header for the first column
        header = CheckableHeader(Qt.Orientation.Horizontal, self.table, list_header_element=self.list_widget_to_header)
        self.table.setHorizontalHeader(header)
        self.scroll_bar = self.table.verticalScrollBar()
        self.scroll_bar.setStyleSheet(
            f'''    
                QScrollBar:vertical {{
                    background-color: transparent;
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: #1C2039;
                    border-radius: 4px;
                    min-height: 10px;
                    margin-right: 1px;
                }}
                QScrollBar::add-line:vertical {{
                    background: none;
                }}
                QScrollBar::sub-line:vertical {{
                    background: none;
                }}
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                    background: none;
                }}
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                    width: 0px;
                    height: 0px;
                    background: none;
                }}
            '''
        )


        self.layout_main.addWidget(self.table)
        self.setLayout(self.layout_main)

    def check_all(self, checked):
        for row in range(self.model_for_table.rowCount()):
            item = self.model_for_table.item(row, 0)
            if item is not None:
                item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)

class TableViewBase(QTableView):
    def __init__(self, callback_onclicked=None):
        super().__init__()
        self.setMouseTracking(True)
        self.hovered_row = -1
        if callback_onclicked is not None:
            self.clicked.connect(callback_onclicked)

    def onClicked(self, index):
        if index.isValid():
            row = index.row()
            print(f"Clicked on row {row}")

    def enterEvent(self, event):
        # self.viewport().update()
        index = self.indexAt(event.pos())
        if index.isValid():
            self.hovered_row = index.row()
            self.viewport().update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered_row = -1
        self.viewport().update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())

        self.hovered_row = index.row()
        self.viewport().update()
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        for row in range(self.model().rowCount()):
            for col in range(self.model().columnCount()):
                if row == self.hovered_row:
                    rect = self.visualRect(self.model().index(row, col))
                    painter.fillRect(rect, QColor(255, 255, 255))
        painter.end()

class CheckableHeader(QHeaderView):
    def __init__(self, orientation, parent=None, list_header_element: dict[int, QWidget] = None):
        super().__init__(orientation, parent)
        if list_header_element is None:
            list_header_element = {}
        self.isChecked = False
        self.list_header_element = list_header_element
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.setStyleSheet('background-color: #1C2039; border-radius: 8px; color: white')

    def paintSection(self, painter, rect, logicalIndex):
        super().paintSection(painter, rect, logicalIndex)
        for index, widget in self.list_header_element.items():
            if index == logicalIndex:
                widget.setParent(self)
                widget.setGeometry(rect)
                widget.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget with Header Checkbox Example")
        self.setGeometry(100, 100, 600, 400)

        button = QPushButton('BUTTON')
        button.clicked.connect(self.check_all)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_all(self):
        dialog = NewAddCameraDialog()
        dialog.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
