# ------------------------------------------------------------------------------------------------------------------------------

# * - To make excutable file out of project use command "pip install pyinstaller" to install important installer files.
# * - to make excutable archive use command "pyinstaller --onefile "File name".py"



import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QLineEdit, QLabel, QHBoxLayout, QCheckBox, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

try:
    import winshell
except ImportError:
    print("Please install the 'winshell' module to interact with the Windows environment.")
    sys.exit(1)


class ImageOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Organizer")
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        self.folder_button = QPushButton("Browse Folder")
        self.folder_button.clicked.connect(self.browse_folder)
        self.top_layout.addWidget(self.folder_button)

        self.check_uncheck_all_button = QPushButton("Check/Uncheck All")
        self.check_uncheck_all_button.clicked.connect(self.check_uncheck_all)
        self.top_layout.addWidget(self.check_uncheck_all_button)

        self.delete_selected_button = QPushButton("Move to Recycle Bin")
        self.delete_selected_button.clicked.connect(self.move_to_recycle_bin)
        self.top_layout.addWidget(self.delete_selected_button)

        self.counter_label = QLabel("Files Collected: 0")
        self.top_layout.addWidget(self.counter_label)

        self.search_button = QPushButton("Search Similar Names")
        self.search_button.clicked.connect(self.search_similar_names)
        self.top_layout.addWidget(self.search_button)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Enter Search Text")
        self.top_layout.addWidget(self.search_line_edit)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.selected_files = []
        self.selected_folder = ""

    def browse_folder(self):
        self.selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.selected_folder:
            self.selected_files.clear()
            self.populate_image_list(self.selected_folder)

    def populate_image_list(self, folder_path):
        # Clear existing layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        for file_name in image_files:
            checkbox = QCheckBox(file_name)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_selected_files)
            self.scroll_layout.addWidget(checkbox)

    def update_selected_files(self):
        self.selected_files = [checkbox.text() for checkbox in self.scroll_widget.findChildren(QCheckBox) if checkbox.isChecked()]
        self.counter_label.setText(f"Files Collected: {len(self.selected_files)}")

    def check_uncheck_all(self):
        all_checked = all([checkbox.isChecked() for checkbox in self.scroll_widget.findChildren(QCheckBox)])
        for checkbox in self.scroll_widget.findChildren(QCheckBox):
            checkbox.setChecked(not all_checked)

    
    def move_to_recycle_bin(self):
        reply = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to permanently delete selected files?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
           for checkbox in self.scroll_widget.findChildren(QCheckBox):
            if checkbox.isChecked():
                file_name = checkbox.text()
                file_path = os.path.join(self.selected_folder, file_name)
                if os.path.exists(file_path):  # Check if the file exists before deleting it
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Failed to delete {file_path}: {str(e)}")
                else:
                    QMessageBox.warning(self, "Error", f"File not found: {file_path}")

        # Update the UI after deletion
        self.update_selected_files()  
        self.populate_image_list(self.selected_folder)


    def search_similar_names(self):
        search_text = self.search_line_edit.text()
        if not search_text:
            QMessageBox.warning(self, "Warning", "Please enter search text")
            return

        for checkbox in self.scroll_widget.findChildren(QCheckBox):
            if search_text.lower() in checkbox.text().lower():
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageOrganizerApp()
    window.show()
    sys.exit(app.exec_())