from PySide6.QtCore import Qt, QEvent, QSize, Signal, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QTabBar, QVBoxLayout, QLabel, QPushButton, QTabWidget, QMainWindow, \
    QHBoxLayout, QStackedLayout, QStackedWidget, QSizePolicy, QLineEdit, QTextEdit, QMenu

from src.custom_title_new.widget.actionable_title_bar import ActionableTitleBar

class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_pos = None
        self.installEventFilter(self)
        self.parent = parent

    def _move(self):
        window_move = self.parent.window().windowHandle()
        window_move.startSystemMove()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            self._move()
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def eventFilter(self, watched, event):
        if watched == self:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                mouse_button = event.button()
                if mouse_button == Qt.LeftButton:
                    # Toggle between full screen and normal mode
                    if self.parent.window().isMaximized():
                        self.parent.window().showNormal()
                    else:
                        self.parent.window().showMaximized()
        return super().eventFilter(watched, event)

class TabWidget(ActionableTitleBar):
    signal_tab_change = Signal(object)
    signal_tab_close = Signal(object)
    signal_add_new_tab = Signal(object)
    signal_close_all_tab = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.__context_menu_p = 0
        self.tab_name_list = set()
        self.__initLastRemovedTabInfo()
        self.__initUi()

    def __initLastRemovedTabInfo(self):
        self.__last_removed_tab_idx = []
        self.__last_removed_tab_widget = []
        self.__last_removed_tab_title = []

    def __initUi(self):
        # Create a QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.installEventFilter(self)
        self.tab_widget.setMaximumHeight(self.tab_widget.tabBar().height())
        self.tab_widget.tabBar().setStyleSheet("""
                     QTabBar {
                        alignment: left;
                    }

                    QTabBar::tab {
                        background-color: lightblue;
                        padding: 8px 12px;
                        font-weight: None;
                    }

                    QTabBar::tab:selected {
                        border-top-left-radius: 4px;
                        border-top-right-radius: 4px;
                        background-color: lightblue;
                        font-weight: bold;
                    }

                    QTabBar::close-button {
                        subcontrol-position: right;
                    }

                    QTabBar::close-button:hover {
                        subcontrol-position: right;
                        border-radius: 2px;
                        font-weight: None;
                    }""")
        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.tabBar().setExpanding(False)
        self.tab_widget.setMovable(False)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.customContextMenuRequested.connect(self.__prepareMenu)
        self.corner_button = QPushButton("ADD +")
        self.tab_widget.setCornerWidget(self.corner_button, Qt.Corner.TopLeftCorner)
        self.tab_widget.setStyleSheet("""
                    QTabWidget::tab-bar {
                        left: 0; 
                    }
                    QTabWidget::pane {
                        background: transparent;
                        border: none;
                    }
                """)

        # Connect the tabCloseRequested signal to a custom slot
        self.corner_button.clicked.connect(self.addNewTab)
        self.tab_bar = self.tab_widget.tabBar()
        self.tab_bar.installEventFilter(self)
        self.tab_bar.currentChanged.connect(self.onTabChange)
        self.tab_bar.tabCloseRequested.connect(self.removeTab)

        layout_tab_widget = QVBoxLayout()
        layout_tab_widget.setContentsMargins(0, 0, 0, 0)
        layout_tab_widget.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout_tab_widget.setSpacing(0)
        layout_tab_widget.addWidget(self.tab_widget)
        self.setLayout(layout_tab_widget)

    def addNewTab(self):
        new_tab_name = self.generate_unique_tab_name()

        # Calculate the index to insert the new tab
        new_tab_index = self.tab_widget.tabBar().count()
        print(f"HanhLT: new_tab_index = {new_tab_index}")
        # Insert the new tab at the calculated index
        self.tab_widget.tabBar().insertTab(new_tab_index, new_tab_name)
        self.signal_add_new_tab.emit(new_tab_index)
        # Activate the newly added tab
        self.tab_bar.setCurrentIndex(new_tab_index)

    def __prepareMenu(self, pos):
        # Get the position of the context menu relative to the QTabWidget
        global_pos = self.tab_widget.mapToGlobal(pos)

        # Get the position of the context menu relative to the QTabBar
        tab_bar = self.tab_widget.tabBar()
        tab_bar_pos = tab_bar.mapFromGlobal(global_pos)
        print(f"HanhLT: tab_bar_pos = {tab_bar_pos}")
        # Retrieve the tab index at the calculated position
        tab_idx = tab_bar.tabAt(tab_bar_pos)
        if tab_idx != -1:
            self.__context_menu_p = tab_bar_pos
            closeTabAction = QAction('Close Tab')
            closeTabAction.triggered.connect(self.closeTab)

            closeAllTabAction = QAction('Close All Tabs')
            closeAllTabAction.triggered.connect(self.closeAllTab)

            closeOtherTabAction = QAction('Close Other Tabs')
            closeOtherTabAction.triggered.connect(self.closeOtherTab)

            closeTabToTheLeftAction = QAction('Close Tabs to the Left')
            closeTabToTheLeftAction.triggered.connect(self.closeTabToLeft)

            closeTabToTheRightAction = QAction('Close Tabs to the Right')
            closeTabToTheRightAction.triggered.connect(self.closeTabToRight)

            # xem kịch bản có cần nút này không? nếu cần thì phải thêm logic bạck lại ui của stacked widget
            reopenClosedTabAction = QAction('Reopen Closed Tab')
            reopenClosedTabAction.triggered.connect(self.reopenClosedTab)

            self.menu = QMenu(self)
            self.menu.addAction(closeTabAction)
            self.menu.addAction(closeAllTabAction)
            self.menu.addAction(closeOtherTabAction)
            self.menu.addAction(closeTabToTheLeftAction)
            self.menu.addAction(closeTabToTheRightAction)
            # self.menu.addAction(reopenClosedTabAction)
            self.menu.exec(self.mapToGlobal(tab_bar_pos))

    def removeTab(self, index):
        # Get the tab name from the tab bar
        tab_name = self.tab_bar.tabText(index)
        # Close the tab in the tab bar
        self.__saveLastRemovedTabInfo(index)
        self.tab_bar.removeTab(index)
        self.signal_tab_close.emit(index)

    def closeTab(self):
        if isinstance(self.__context_menu_p, QPoint):
            tab_idx = self.tab_widget.tabBar().tabAt(self.__context_menu_p)
            print(f"HanhLT: tab_idx = {tab_idx}")
            self.removeTab(tab_idx)
            self.__context_menu_p = 0
        else:
            self.removeTab(self.tab_bar.currentIndex())

    def closeAllTab(self):
        tab_bar = self.tab_widget.tabBar()
        num_tabs = tab_bar.count()

        # Remove each tab from the QTabBar
        for i in range(num_tabs):
            tab_bar.removeTab(0)  # Remove the tab at index 0 each time, as the index of tabs will change after removal
        self.tab_name_list.clear()

        self.addNewTab()

    def closeOtherTab(self):
        if isinstance(self.__context_menu_p, QPoint):
            tab_idx = self.tab_bar.tabAt(self.__context_menu_p)
            self.__removeTabFromLeftTo(tab_idx)
            tab_idx = 0
            self.tab_bar.setCurrentIndex(tab_idx)
            self.__removeTabFromRightTo(tab_idx)

    def closeTabToLeft(self):
        if isinstance(self.__context_menu_p, QPoint):
            tab_idx = self.tab_bar.tabAt(self.__context_menu_p)
            self.__removeTabFromLeftTo(tab_idx)

    def __removeTabFromLeftTo(self, idx):
        for i in range(idx - 1, -1, -1):
            self.removeTab(i)

    def __removeTabFromRightTo(self, idx):
        for i in range(self.tab_bar.count() - 1, idx, -1):
            self.removeTab(i)

    def closeTabToRight(self):
        if isinstance(self.__context_menu_p, QPoint):
            tab_idx = self.tab_bar.tabAt(self.__context_menu_p)
            self.__removeTabFromRightTo(tab_idx)

    def __saveLastRemovedTabInfo(self, idx):
        self.__last_removed_tab_idx.append(idx)
        # self.__last_removed_tab_widget.append(self.widget(idx))
        self.__last_removed_tab_title.append(self.tab_bar.tabText(idx))

    def reopenClosedTab(self):
        # todo enable/disable action dynamically by existence of closed tab
        if len(self.__last_removed_tab_idx) > 0:
            for i in range(len(self.__last_removed_tab_idx) - 1, -1, -1):
                self.tab_bar.insertTab(self.__last_removed_tab_idx[i],
                                       self.__last_removed_tab_title[i])
            self.tab_bar.setCurrentIndex(self.__last_removed_tab_idx[-1])
            self.__initLastRemovedTabInfo()

    def onTabChange(self, index):
        self.signal_tab_change.emit(index)

    def generate_unique_tab_name(self):
        # Generate a unique tab name
        tab_name_base = "Tab"
        count = 1
        while True:
            tab_name = f"{tab_name_base} {count}"
            if tab_name not in self.tab_name_list:
                break
            count += 1
        # Add the tab name to the set of existing names
        self.tab_name_list.add(tab_name)
        return tab_name

    def eventFilter(self, watched, e):
        if watched.objectName() == "tab_widget":
            if e.type() == QEvent.Type.MouseButtonPress:
                mouse_button = e.button()
                if mouse_button == Qt.MouseButton.MiddleButton:
                    global_pos = self.tab_widget.mapToGlobal(e.position())
                    print(f"HanhLT: global_pos = {global_pos}")
                    # Get the position of the context menu relative to the QTabBar
                    tab_bar = self.tab_widget.tabBar()
                    tab_bar_pos = tab_bar.mapFromGlobal(global_pos)
                    print(f"HanhLT: tab_bar_pos = {tab_bar_pos}")
                    # Retrieve the tab index at the calculated position
                    tab_idx = tab_bar.tabAt(tab_bar_pos.toPoint())
                    print(f"HanhLT: tab_idx = {tab_idx}")

                    if tab_idx != -1:
                        # Close the tab
                        self.tab_bar.tabCloseRequested.emit(tab_idx)
                        return True
            # if e.modifiers() & Qt.AltModifier and e.key() == Qt.Key_Left:
            #     self.tab_widget.tabBar().setCurrentIndex(self.tab_widget.tabBar().currentIndex() - 1)
            # elif e.modifiers() & Qt.AltModifier and e.key() == Qt.Key_Right:
            #     self.tab_widget.tabBar().setCurrentIndex(self.tab_widget.tabBar().currentIndex() + 1)
            # elif e.modifiers() & Qt.ControlModifier and e.key() == Qt.Key_F4:
            #     self.closeTab()

        return super().eventFilter(watched, e)

class CustomTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        pass

    def addNewTab(self):
        pass

    def deleteTab(self):
        pass

    def tabChangeEvent(self):
        pass

    def clearTab(self):
        pass

    def count(self):
        pass

    def currentTabIndex(self):
        pass

    def setCurrentTabIndex(self):
        pass


class TabBarExample(QMainWindow):

    """
    Tạo, lưu và quản lý tab cũng như widget của Tab > lấy ra đúng Tab và widget, truy xuất vào dict đúng tab
    Close current tab
    Close tab to left
    Close tab to right
    Close all tab
    Close others tab"""

    '''Add new tab
    Open existing tab
    Delete existing tab
    Edit tab name > update in dict
    
    '''

    def __init__(self):
        super().__init__()
        # Create a set to store existing tab names
        self.existing_tab_names = set()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle('Frameless Window with Rounded Corners')
        self.setWindowTitle('QTabBar Example')
        self.setGeometry(100, 100, 400, 300)
        self.initUi()

    def initUi(self):
        # Create a QStackedLayout to manage content widgets
        self.stacked_widget = QStackedWidget()
        self.custom_tab_widget = TabWidget(self)
        self.custom_tab_widget.setFixedHeight(32)
        self.custom_tab_widget.signal_add_new_tab.connect(self.addNewTab)
        self.custom_tab_widget.signal_tab_change.connect(self.tab_changed)
        self.custom_tab_widget.signal_tab_close.connect(self.close_tab)
        self.custom_tab_widget.addNewTab()

        # Set the main layout for the widget
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(0)
        self.main_widget.setLayout(main_layout)

        layout_body = QHBoxLayout()
        layout_body.setContentsMargins(0, 0, 0, 0)
        layout_body.addWidget(QTextEdit("Tree View"), 2)
        layout_body.addWidget(self.stacked_widget, 8)
        widget_body = QWidget()
        widget_body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        widget_body.setLayout(layout_body)

        main_layout.addWidget(self.custom_tab_widget)
        main_layout.addWidget(widget_body)
        self.setCentralWidget(self.main_widget)

    def addNewTab(self, idx):
        new_content_widget = QTextEdit(f"Content of Tab {idx}")
        new_content_widget.hide()
        print(f"HanhLT: index = {idx}")
        # Store the content widget in the QStackedLayout
        self.stacked_widget.addWidget(new_content_widget)
        print(f"HanhLT: self.stacked_widget = {self.stacked_widget.widget(idx)}")
        # Show the corresponding content widget
        self.tab_changed(idx)

    def close_tab(self, index):
        # # Get the tab name from the tab bar
        # tab_name = self.tab_bar.tabText(index)
        # self.tab_contents.remove(tab_name)  # Option
        # # Close the tab in the tab bar
        # self.tab_bar.removeTab(index)

        self.stacked_widget.removeWidget(self.stacked_widget.widget(index))
        self.stacked_widget.setCurrentIndex(self.custom_tab_widget.tab_bar.currentIndex())

        # # Check if the tab name is in the set before removing it
        # if tab_name in self.existing_tab_names:
        #     self.existing_tab_names.remove(tab_name)

    def tab_changed(self, index):
        # Show the corresponding content widget when a tab is selected
        self.stacked_widget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication([])
    window = TabBarExample()
    window.showMaximized()
    window.show()
    app.exec()
