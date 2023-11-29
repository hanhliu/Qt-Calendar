import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QCheckBox

import sys

from PySide6.QtGui import QImage
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget,  QVBoxLayout, QLabel, QHBoxLayout

class CustomQCheckBox(QCheckBox):
    def __init__(self, title, type_checkbox):
        super().__init__()
        self.title = title
        self.type_checkbox = type_checkbox
        self.init_ui()

    def init_ui(self):
        self.setText(self.title)
        self.setChecked(False)

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui()

    def load_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_one = []
        self.list_two = []
        # Create four QCheckBox widgets with labels
        self.voice_cb = CustomQCheckBox("Voice", "voice")
        self.alarm_cb = CustomQCheckBox("Alarm", "alarm")
        self.notification_cb = CustomQCheckBox("Notification", "notification")
        self.highlight_cb = CustomQCheckBox("Highlight", "highlight")
        self.list_one.append(self.voice_cb)
        self.list_one.append(self.alarm_cb)
        self.list_one.append(self.notification_cb)
        self.list_one.append(self.highlight_cb)

        # Connect the stateChanged signals to a slot function
        self.voice_cb.stateChanged.connect(self.checkbox_warning_method_change)
        self.alarm_cb.stateChanged.connect(self.checkbox_warning_method_change)
        self.notification_cb.stateChanged.connect(self.checkbox_warning_method_change)
        self.highlight_cb.stateChanged.connect(self.checkbox_warning_method_change)

        # Create four QCheckBox widgets with labels
        self.ivms_cb = CustomQCheckBox("VMS", "ivms")
        self.iems_cb = CustomQCheckBox("EMS", "iems")
        self.tactical_cb = CustomQCheckBox("Tactical", "tactical")
        self.internal_sms_cb = CustomQCheckBox("Internal SMS", "inter_sms")
        self.internal_email_cb = CustomQCheckBox("Internal Email", "inter_mail")
        self.external_sms_cb = CustomQCheckBox("External SMS", "ext_sms")
        self.external_email_cb = CustomQCheckBox("External Email", "ext_mail")
        self.telegram_cb = CustomQCheckBox("Telegram", "telegram")
        self.list_two.append(self.ivms_cb)
        self.list_two.append(self.iems_cb)
        self.list_two.append(self.tactical_cb)
        self.list_two.append(self.internal_sms_cb)
        self.list_two.append(self.internal_email_cb)
        self.list_two.append(self.external_sms_cb)
        self.list_two.append(self.external_email_cb)
        self.list_two.append(self.telegram_cb)

        # Connect the stateChanged signals to a slot function
        self.ivms_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.iems_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.tactical_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.internal_sms_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.internal_email_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.external_sms_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.external_email_cb.stateChanged.connect(self.checkbox_alert_channel_change)
        self.telegram_cb.stateChanged.connect(self.checkbox_alert_channel_change)

        self.label_one = QLabel("1. Methods")
        self.label_two = QLabel("2. Channels")
        layout.addWidget(self.label_one)
        layout.addWidget(self.voice_cb)
        layout.addWidget(self.alarm_cb)
        layout.addWidget(self.notification_cb)
        layout.addWidget(self.highlight_cb)
        layout.addWidget(self.label_two)
        layout.addWidget(self.ivms_cb)
        layout.addWidget(self.iems_cb)
        layout.addWidget(self.tactical_cb)
        layout.addWidget(self.internal_sms_cb)
        layout.addWidget(self.internal_email_cb)
        layout.addWidget(self.external_sms_cb)
        layout.addWidget(self.external_email_cb)
        layout.addWidget(self.telegram_cb)

        num_checked_in_list_one = sum(1 for item in self.list_one if item.isChecked())
        if num_checked_in_list_one == 0:  # If no checkboxes in list_one are checked
            # Clear all checked checkboxes in list_two and disable them
            for item in self.list_two:
                if item.isChecked():
                    item.setChecked(False)
                item.setDisabled(True)

        self.setLayout(layout)

    def checkbox_warning_method_change(self, state):
        sender = self.sender()  # Get the checkbox that emitted the signal
        if state == 2:  # Checked state
            checked_position = self.list_one.index(sender)
            if checked_position == 0:  # voice
                checked_items = []
                if self.voice_cb.isChecked():
                    self.alarm_cb.setChecked(False)
                if not self.highlight_cb.isChecked():
                    for index, item in enumerate(self.list_two):
                        if item.type_checkbox == "ivms" or item.type_checkbox == "iems" \
                                or item.type_checkbox == "tactical":
                            item.setEnabled(True)
                        else:
                            item.setEnabled(False)
                        if item.isChecked():
                            checked_items.append(item)

                    # If more than one checkbox is checked, clear all except the first one
                    if len(checked_items) > 1:
                        for i, item in enumerate(checked_items):
                            if i != 0:  # Clear all except the first one
                                item.setChecked(False)

                # for item in self.list_two:
                #     item.setChecked(False)

            elif checked_position == 1:  # alarm sound
                checked_items = []
                if self.alarm_cb.isChecked():
                    self.voice_cb.setChecked(False)
                if not self.highlight_cb.isChecked():
                    for index, item in enumerate(self.list_two):
                        if item.type_checkbox == "ivms" or item.type_checkbox == "iems" \
                                or item.type_checkbox == "tactical":
                            item.setEnabled(True)
                        else:
                            item.setEnabled(False)
                        if item.isChecked():
                            checked_items.append(item)

                    # If more than one checkbox is checked, clear all except the first one
                    if len(checked_items) > 1:
                        for i, item in enumerate(checked_items):
                            if i != 0:  # Clear all except the first one
                                item.setChecked(False)

            elif checked_position == 2:  # noti message
                for item in self.list_two:
                    if not self.highlight_cb.isChecked() and (self.alarm_cb.isChecked() or self.voice_cb.isChecked()):
                        if item.type_checkbox == "ivms" or item.type_checkbox == "iems" \
                                or item.type_checkbox == "tactical":
                            item.setEnabled(True)
                        else:
                            item.setEnabled(False)
                    elif self.highlight_cb.isChecked():
                        if item.type_checkbox != "ivms":
                            item.setDisabled(True)
                    else:
                        if not item.isEnabled():
                            item.setEnabled(True)
            elif checked_position == 3:  # 2light
                for item in self.list_two:
                    if not item.isEnabled() and item.type_checkbox == "ivms":
                        item.setDisabled(False)
                    elif item.isEnabled() and item.type_checkbox != "ivms":
                        item.setDisabled(True)
                        item.setChecked(False)
        else:
            num_checked_in_list_one = sum(1 for item in self.list_one if item.isChecked())
            if num_checked_in_list_one == 0:  # If no checkboxes in list_one are checked
                # Clear all checked checkboxes in list_two and disable them
                for item in self.list_two:
                    if item.isChecked():
                        item.setChecked(False)
                    item.setDisabled(True)
            else:  # At least one checkbox
                checked_position = self.list_one.index(sender)
                if checked_position == 0:
                    for item in self.list_two:
                        if self.notification_cb.isChecked() and not self.highlight_cb.isChecked():
                            item.setEnabled(True)

                elif checked_position == 1:
                    for item in self.list_two:
                        if self.notification_cb.isChecked() and not self.highlight_cb.isChecked():
                            item.setEnabled(True)
                elif checked_position == 2:
                    print("HanhLT: uncheck noti")
                    for item in self.list_two:
                        if self.highlight_cb.isChecked():
                            if item.type_checkbox == "ivms":
                                item.setEnabled(True)
                            else:
                                item.setEnabled(False)
                        elif self.alarm_cb.isChecked() or self.voice_cb.isChecked():
                            if item.type_checkbox == "ivms" or item.type_checkbox == "iems" \
                                    or item.type_checkbox == "tactical":
                                item.setEnabled(True)
                            else:
                                item.setEnabled(False)
                elif checked_position == 3:
                    print("HanhLT: uncheck 2light")
                    for item in self.list_two:
                        if self.alarm_cb.isChecked() or self.voice_cb.isChecked():
                            if item.type_checkbox == "ivms" or item.type_checkbox == "iems" \
                                    or item.type_checkbox == "tactical":
                                item.setEnabled(True)
                            else:
                                item.setEnabled(False)
                        else:
                            item.setDisabled(False)

    def checkbox_alert_channel_change(self, state):
        sender = self.sender()  # Get the checkbox that emitted the signal
        if self.voice_cb.isChecked() or self.alarm_cb.isChecked():
            if state == 2:
                for checkbox in self.list_two:
                    if checkbox != sender:
                        checkbox.setChecked(False)
        elif self.notification_cb.isChecked():
            print("HanhLT: allow pick multi checkbox")
        elif self.highlight_cb.isChecked():
            print("HanhLT: just pick VMS")



class CheckBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CheckBox Example")
        self.setGeometry(100, 100, 400, 400)

        central_widget = HomeScreen()
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CheckBoxExample()
    main_window.show()
    sys.exit(app.exec())
