# import sys
# from os.path import basename
# from PyQt5.QtCore import QPoint, Qt, QRect
# from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog, QLabel, QTextEdit, QVBoxLayout
# from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QFont
# import SnippingMenu
# import test
#
#
# class MenuResponse(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # self.window = QMainWindow()
#         # self.window.setWindowTitle("New Windows")
#         # self.window.label = QLabel('This is Text', self.window)
#         #
#         # # self.window = submittinPictutre.Sub_Menu()
#         # # self.ui = Sub_Menu()
#         # # self.window.show()
#         # # label = QLabel("This Is Text", self.window)
#         # self.window.label.resize(350, 50)
#         # # self.window.label.setStyleSheet("border: 5px solid black;")
#         # self.window.label.setFont(QFont('Arial', 20))
#         # self.window.show()
#         self.drawing = False
#         self.brushSize = 3
#         self.brushColor = Qt.red
#         self.lastPoint = QPoint()
#         self.total_snips = 0
#         self.title = "Title"
#         # self.setFixedWidth(300)
#         # self.setFixedHeight(100)
#         self.setMinimumHeight(200)
#         # label = QLabel('Hello Widgets!', self)
#         # textedit = QTextEdit(
#         #     self,
#         #     acceptRichText=False,
#         #     lineWrapMode= QTextEdit.FixedColumnWidth,
#         #     lineWrapColumnOrWidth=25,
#         #     placeholderText='Enter your text here'
#         # )
#         self.setMinimumWidth(400)
#         self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
#         # #Adding Labels
#         label = QLabel('Hello Widgets!', self)
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#         layout.addWidget(label)
#         # layout.addWidget(line_edit)
#
#         # SHOWING
#         self.show()
#
#
#
# def start():
#     app = QApplication(sys.argv)
#     mainMenu = MenuResponse()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     start()
#     # test.run()
#     # SnippingMenu.Menu()
#
#
#
