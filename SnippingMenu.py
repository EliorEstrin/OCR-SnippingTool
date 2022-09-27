import sys
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog, QLabel, QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QFont
import SnippingTool
import handWriteRecognizion
import numpy as np


class Menu(QMainWindow):
    """
    This is the class for the main application window.
    It contains all buttons and UI desing.
    """
    COLORS = ['Red', 'Black', 'Blue', 'Green', 'Yellow']
    SIZES = [1, 3, 5, 7, 9, 11]
    default_title = "Snipping Tool"

    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, snip_number=None, start_position=(300, 300, 350, 250)):
        super().__init__()
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.red
        self.lastPoint = QPoint()
        self.total_snips = 0
        self.title = Menu.default_title
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
        self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')

        #sumbit button code(Get Text button) >> Button to call the api
        self.button = QPushButton("Get Text", self)
        self.button.setMinimumWidth(10)
        self.button.setFixedHeight(30)
        self.button.move(0, 160)
        #setting a value for img in case it is the first run
        img = numpy_image
        if img is None:
            img = " "
        else:
            img = numpy_image
        #Connecting the Click of the button with function
        self.button.clicked.connect(lambda: self.get_img_response(img))

        # New snip button Code
        new_snip_action = QAction('New', self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('Snip!')
        new_snip_action.triggered.connect(self.new_image_window)

        # Brush color
        brush_color_button = QPushButton("Brush Color")
        colorMenu = QMenu()
        for color in Menu.COLORS:
            colorMenu.addAction(color)
        brush_color_button.setMenu(colorMenu)
        colorMenu.triggered.connect(lambda action: change_brush_color(action.text()))

        # Brush Size
        brush_size_button = QPushButton("Brush Size")
        sizeMenu = QMenu()
        for size in Menu.SIZES:
            sizeMenu.addAction("{0}px".format(str(size)))
        brush_size_button.setMenu(sizeMenu)
        sizeMenu.triggered.connect(lambda action: change_brush_size(action.text()))

        # Save button Code
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save')
        save_action.triggered.connect(self.save_file)

        # Exit button Code
        exit_window = QAction('Exit', self)
        exit_window.setShortcut('Ctrl+Q')
        exit_window.setStatusTip('Exit application')
        exit_window.triggered.connect(self.close)

        #adding buttons to tools bar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_snip_action)
        self.toolbar.addAction(save_action)
        self.toolbar.addWidget(brush_color_button)
        self.toolbar.addWidget(brush_size_button)
        self.toolbar.addAction(exit_window)

        self.snippingTool = SnippingTool.SnippingWidget()
        self.setGeometry(*start_position)

        # From the second initialization, both arguments will be valid
        if numpy_image is not None and snip_number is not None:
            self.image = self.convert_numpy_img_to_qpixmap(numpy_image)
            self.change_and_set_title("Snip #{0}".format(snip_number))
        else:
            self.image = QPixmap("background.PNG")
            self.change_and_set_title(Menu.default_title)

        self.resize(self.image.width(), self.image.height() + self.toolbar.height())
        self.show()

        def change_brush_color(new_color):
            self.brushColor = eval("Qt.{0}".format(new_color.lower()))

        def change_brush_size(new_size):
            self.brushSize = int(''.join(filter(lambda x: x.isdigit(), new_size)))

    # snippingTool.start() will open a new window, so if this is the first snip, close the first window.
    def new_image_window(self):
        if self.snippingTool.background:
            self.close()
        self.total_snips += 1
        self.snippingTool.start()


    def get_img_response(self, img):
        """
            #Important Function - Called On Sumbit Click
            #Basically we are creating a new windows with a textbox
            #And setting the value of the textbox to the returned string from the
            """
        self.window = QMainWindow()
        self.window.setWindowTitle("New Windows")
        self.window.setMinimumHeight(200)
        self.window.setMinimumWidth(400)
        self.window.label = QLabel('AI Text: ', self.window)
        self.window.label.setFont(QFont('Arial', 20))
        self.textbox = QPlainTextEdit(self.window)
        self.textbox.move(10,30)
        self.textbox.resize(280, 120)
        self.window.show()

        # self.textbox = QLineEdit(self.window)
        # self.textbox.setText("Text")
        # self.textbox.move(10, 30)
        # self.textbox.resize(280, 120)
        # print(type(img))
        # print(type(numpy.array()))
        #Saving The image
        # print(f"Type A {type(img)}  Type B: {type(numpy.array())}")


        self.textbox.setPlainText("Text")

        if isinstance(img, (np.ndarray, np.generic)):
            # print(img)
            # print(type(img))
            print("Saving THe image:")
            from PIL import Image
            im = Image.fromarray(img)
            im.save("some_image.jpeg")
            #Calling The API
            text = handWriteRecognizion.get_text_from_image()
            self.textbox.setPlainText(text)
        else:
            print("This is The run number 0 - No image")


    def save_file(self):
        file_path, name = QFileDialog.getSaveFileName(self, "Save file", self.title, "PNG Image file (*.png)")
        if file_path:
            self.image.save(file_path)
            self.change_and_set_title(basename(file_path))
            print(self.title, 'Saved')

    def change_and_set_title(self, new_title):
        self.title = new_title
        self.setWindowTitle(self.title)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0, self.toolbar.height(), self.image.width(), self.image.height())
        painter.drawPixmap(rect, self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos() - QPoint(0, self.toolbar.height()))
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    # TODO exit application when we exit all windows
    def closeEvent(self, event):
        event.accept()

    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())


# def open_respone():
#     # mainMenu2 = test.App()
#     # return mainMenu2
#     app = QApplication(sys.argv)
#     main = Menu()
#     # mainMenu2 = test.App()
#
#     # open_respone()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    # mainMenu2 = test.App()
    # main3 = open_respone()
    # open_respone()
    sys.exit(app.exec_())
