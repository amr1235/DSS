from PyQt5.QtWidgets import (QApplication, QWidget,QMainWindow,
                             QFileDialog, QGridLayout, QVBoxLayout, QMessageBox, QShortcut, QMenuBar)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import imageio.v2 as io
import sys

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.Grid = QGridLayout(self)
        self.view = pg.ImageView()
        self.Grid.addWidget(self.view)
        # drag and drop 
        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            try : 
                file_path = event.mimeData().urls()[0].toLocalFile()
                image = io.imread(file_path)
                self.view.setImage(image)
            except:
                QMessageBox.critical(self, "error", "Something went wrong!")

            event.accept()
        else:
            event.ignore()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.mainLayout = QVBoxLayout()
        central_widget.setLayout(self.mainLayout)

        self.setWindowTitle("Amr Aly")

        # create menu bar action 
        menuBar = QMenuBar(self)
        self.file_action = menuBar.addAction("file")
        self.setMenuBar(menuBar)
        self.file_action.triggered.connect(self.open_image)
        # add pyqtgraph widget
        self.image_viewer = ImageViewer()
        self.mainLayout.addWidget(self.image_viewer)
        # add saving rotuine
        self.image_path = None
        self.save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.save_shortcut.activated.connect(self.save_image)

        

    def open_image(self) : 
        file_path, _ = QFileDialog.getOpenFileName(filter="*.png *.jpg")
        if file_path:
            self.image_path = file_path
            self.image = io.imread(file_path)
            self.image_viewer.view.setImage(self.image)
        else: 
            QMessageBox.critical(self, "error", "Something went wrong!")

    def save_image(self) :
        try : 
            self.image_viewer.view.export("Image.png")
            QMessageBox.information(self, "Image Saved", "Image succesfully Saved!")
        except:
            QMessageBox.critical(self, "error", "Something went wrong!")


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()