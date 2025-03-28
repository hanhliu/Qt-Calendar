import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileDialog, QWidget, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt


class ImageTextEditor(QMainWindow):
    def __init__(self, input_path="./"):
        super().__init__()
        self.input_path = input_path
        self.current_index = 0
        self.file_paths = {}
        self.history = {}
        self.handle_file = []
        self.current_font_size = 23  # Default font size
        self.load_handle()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Text Editor")
        self.setGeometry(100, 100, 1024, 600)

        # Layout
        main_layout = QVBoxLayout()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(main_layout)

        # Folder Selection Button
        folder_layout = QHBoxLayout()
        main_layout.addLayout(folder_layout)

        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_folder_button)

        self.folder_path_label = QLabel(f"Current Folder: {self.input_path}")
        folder_layout.addWidget(self.folder_path_label)

        # File Name Label
        self.filename_label = QLabel()
        self.filename_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.filename_label)
        # Image Display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Text Editor
        self.text_edit = QTextEdit()
        self.set_text_font()
        main_layout.addWidget(self.text_edit)

        # Connect textChanged signal to update length
        self.text_edit.textChanged.connect(self.update_text_length)

        # Font Size and Text Length Control (in the same row)
        font_length_layout = QHBoxLayout()
        main_layout.addLayout(font_length_layout)

        # Font Size Control
        font_size_label = QLabel("Font Size:")
        font_length_layout.addWidget(font_size_label)

        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(10, 50)  # Set reasonable range
        self.font_size_spinbox.setValue(self.current_font_size)
        self.font_size_spinbox.valueChanged.connect(self.change_font_size)
        font_length_layout.addWidget(self.font_size_spinbox)

        # Stretch to push next widget to the right
        font_length_layout.addStretch(1)

        # Text Length Label
        self.text_length_label = QLabel("Text Length: 0")
        font_length_layout.addWidget(self.text_length_label)

        # Buttons
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next)
        button_layout.addWidget(self.next_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_file)
        button_layout.addWidget(self.delete_button)

        self.load_files()

    def select_folder(self):
        # Save current text if any
        if self.file_paths:
            self.save_text()

        # Open folder selection dialog
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            # Reset all data
            self.input_path = folder
            self.current_index = 0
            self.file_paths.clear()
            self.history.clear()

            # Update folder path label
            self.folder_path_label.setText(f"Current Folder: {self.input_path}")

            # Reload files from the new folder
            self.load_files()

    def load_files(self):
        directory = self.input_path

        # Clear existing files
        self.file_paths.clear()
        self.history.clear()

        # Load files from the directory
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                if filename.endswith(".jpg"):
                    self.file_paths[filename] = filepath
                elif filename.endswith(".txt"):
                    with open(filepath, "r") as f:
                        self.history[filename] = f.read()

        # Handle empty directory
        if not self.file_paths:
            self.image_label.clear()
            self.filename_label.setText("No images found in the selected folder")
            self.text_edit.clear()
            self.text_length_label.setText("Text Length: 0")
            return

        # Find first unhandled image
        while True:
            image_path = sorted(self.file_paths.keys())[self.current_index]
            if self.file_paths[image_path] in self.handle_file:
                self.current_index = min(self.current_index + 1, len(self.file_paths) - 1)
            else:
                break

        self.show_current_image_and_text()

    def save_history(self, image_path):
        self.handle_file.append(image_path)
        with open("./history.txt", "w") as file:
            for string in self.handle_file:
                file.write(string + "\n")

    def show_current_image_and_text(self):
        if not self.file_paths:
            return

        image_filename = sorted(self.file_paths.keys())[self.current_index]
        image_path = self.file_paths[image_filename]
        self.image_label.setPixmap(QPixmap(image_path))
        self.filename_label.setText(f"Current File: {image_filename}")

        if image_path not in self.handle_file:
            self.save_history(image_path)

        text_filename = image_filename.replace(".jpg", ".txt")
        if text_filename in self.history:
            text_content = self.history[text_filename]
            self.text_edit.setText(text_content)
            self.text_length_label.setText(f"Text Length: {len(text_content)}")
        else:
            self.text_edit.clear()
            self.text_length_label.setText("Text Length: 0")

    def show_previous(self):
        if not self.file_paths:
            return

        self.save_text()
        self.current_index = max(self.current_index - 1, 0)
        self.show_current_image_and_text()

    def show_next(self):
        if not self.file_paths:
            return

        self.save_text()
        self.current_index = min(self.current_index + 1, len(self.file_paths) - 1)
        self.show_current_image_and_text()

    def save_text(self):
        if not self.file_paths:
            return

        image_filename = sorted(self.file_paths.keys())[self.current_index]
        text_filename = self.file_paths[image_filename].replace(".jpg", ".txt")
        text_content = self.text_edit.toPlainText()
        print(text_filename)
        self.history[image_filename.replace(".jpg", ".txt")] = text_content

        with open(text_filename, "w") as f:
            f.write(text_content)

        print(f"Saved text for {image_filename}")

    def delete_file(self):
        if len(self.file_paths) == 0:
            QMessageBox.information(self, 'Info', f'No file')
            return

        image_filename = sorted(self.file_paths.keys())[self.current_index]
        image_path = self.file_paths[image_filename]
        text_filename = image_path.replace(".jpg", ".txt")

        # Confirm deletion with the user
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                     f'Are you sure you want to delete "{image_filename}" and the associated text file?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Delete the image file
            os.remove(image_path)
            # Delete the text file
            os.remove(text_filename)
            # Remove the file from the history
            self.handle_file.remove(image_path)
            with open("./history.txt", "w") as file:
                for string in self.handle_file:
                    file.write(string + "\n")
            del self.file_paths[image_filename]
            del self.history[image_filename.replace(".jpg", ".txt")]

            # Handle empty directory after deletion
            if not self.file_paths:
                self.image_label.clear()
                self.filename_label.setText("No images found in the selected folder")
                self.text_edit.clear()
                self.text_length_label.setText("Text Length: 0")
                return

            # Move to the next image
            self.current_index = min(self.current_index, len(self.file_paths) - 1)
            if self.current_index == len(self.file_paths) and self.current_index > 0:
                self.current_index -= 1
            self.show_current_image_and_text()

    def load_handle(self):
        if os.path.exists("history.txt"):
            with open("history.txt", "r") as f:
                for line in f:
                    filename = line.strip()
                    self.handle_file.append(filename)

    def update_text_length(self):
        # Get the current text and update the length label in real-time
        text_content = self.text_edit.toPlainText()
        self.text_length_label.setText(f"Text Length: {len(text_content)}")

    def set_text_font(self):
        # Set font with current font size and letter spacing
        font = QFont("Arial", self.current_font_size)
        font.setLetterSpacing(QFont.PercentageSpacing, 120)  # Increase character spacing by 120%
        self.text_edit.setFont(font)

    def change_font_size(self, size):
        # Update current font size and apply to text edit
        self.current_font_size = size
        self.set_text_font()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageTextEditor()
    window.show()
    sys.exit(app.exec())
