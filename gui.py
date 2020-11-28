from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QFileSystemModel, QTreeView, QVBoxLayout
from PyQt5.QtCore import QDir, QModelIndex, QRect
from PyQt5.QtGui import QPixmap
import sys
from ui_imageviewerwindow import Ui_ImageViewer
from ui_mainwindow import Ui_MainWindow
from pathlib import Path
from downloader import WallpaperDownloader


class ImageViewer(QtWidgets.QMainWindow, Ui_ImageViewer):
    def __init__(self, folder_path, configuration, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.folder_path = folder_path
        self.image_size = configuration[0].split('x')
        self.setupUi(self)
        
        self.width = int(self.image_size[0])
        self.height = int(self.image_size[1])
        self.aspect_ratio = (self.height / self.width) * 900
        
        self.resize(900 + 211, int(self.aspect_ratio))
        self.label.setGeometry(QtCore.QRect(211, -5, 900, int(self.aspect_ratio)))
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.folder_view.setModel(self.model)
        self.folder_view.setRootIndex(self.model.index(self.folder_path))
        self.folder_view.selectionModel().selectionChanged.connect(self.file_details)
        self.folder_view.setGeometry(QtCore.QRect(0, 0, 211, int(self.aspect_ratio)))


    def file_details(self):
        index = self.folder_view.currentIndex()
        image = self.model.filePath(index)
        self.label.setPixmap(QPixmap(image))



class WallpaperApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(WallpaperApp, self).__init__(parent)
        self.setupUi(self)
        self.folder_path = None
        self.configuration = []
        self.groupBox_type_of_download.setDisabled(True)
        self.search_bar.textChanged.connect(self.change_button_status)
        self.search_button.clicked.connect(self.search_terms)
        self.download_button.clicked.connect(self.download)
        self.user_search = None
        self.folder_path = None
        
        # List and display all the radio buttons in a groupBox
        self.radio_buttons = self.groupBox_resolution.findChildren(QtWidgets.QRadioButton)
        for self.radio_button in self.radio_buttons:
            self.radio_button.toggled.connect(self.radio_button_logic)

    def button_control(self, on_or_off):
        self.groupBox_5_4.setDisabled(on_or_off)
        self.groupBox_16_9.setDisabled(on_or_off)
        self.groupBox_4_3.setDisabled(on_or_off)
        self.groupBox_16_10.setDisabled(on_or_off)
        self.groupBox_ultrawide.setDisabled(on_or_off)

    def radio_button_logic(self):
        self.button_control(True)
        self.groupBox_type_of_download.setDisabled(False)
        radio_toggle = self.sender()
        if radio_toggle.isChecked():
            self.configuration.append(radio_toggle.text())
            if len(self.configuration) > 1:
                self.groupBox_type_of_download.setDisabled(True)
                self.downloading_update_label.setText(f'Resolution: {self.configuration[0]}\n{self.configuration[1]}')

    def change_button_status(self):

        if len(self.search_bar.text()) > 0:
            return self.activate_buttons()
        else:

            return self.disable_buttons()

    def activate_buttons(self):
        self.search_button.setDisabled(False)
        self.download_button.setDisabled(False)

    def disable_buttons(self):
        self.search_button.setDisabled(True)
        self.download_button.setDisabled(True)

    def create_and_open_folder(self):
        folder_dialog = QFileDialog()
        self.folder_path = folder_dialog.getExistingDirectory(None, "Select Folder")
        return self.folder_path

    def search_terms(self):
        self.create_and_open_folder()
        self.user_search = WallpaperDownloader(self.search_bar.text(), self.configuration[0], self.folder_path)
        self.downloading_update_label.setText(self.user_search.number_of_wallpapers)
        self.user_search.search()

        return self.downloading_update_label.setText(f'{len(self.user_search.number_of_wallpapers)} Wallpapers Found')

    def download(self):
        self.dialog = ImageViewer(self.folder_path, self.configuration)
        self.dialog.show()
        self.user_search.download_content(self.configuration[1])

def main():
    app = QApplication(sys.argv)
    form = WallpaperApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
