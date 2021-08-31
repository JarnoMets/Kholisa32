# This Python file uses the following encoding: utf-8
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow, QMenu, QAction
from PySide2.QtGui import QColor, QColorConstants
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import SIGNAL, QObject, QFile, QIODevice

from compiler import Compiler
from link import Linker
from uart import Uart

class mainwindow(QMainWindow):
    save_loc: str = None
    save_name: str = None
    saved: bool = True

    build_loc: str = None
    build_name: str = None
    build: bool = False

    def __init__(self):
        QMainWindow.__init__(self)

    def init():
        font = window.editor.document().defaultFont()
        font.setPixelSize(15)
        window.editor.document().setDefaultFont(font)
        window.editor.setTabStopWidth(20)

    def exit():
        if mainwindow.saved == False:
            msgBox = QMessageBox(QMessageBox.Question, "Save", "Save file?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.Yes)

            ans = msgBox.exec_()

            if ans == QMessageBox.Yes:
                mainwindow.save()
            elif ans == QMessageBox.No:
                return
            else:
                return

    def compile() -> str:
        Compiler.errors = []
        output = Compiler.compile(window.editor.toPlainText())
        if Compiler.errors:
            window.buildLog.setText("\n".join(Compiler.errors))
            return None
        else:
            window.buildLog.setText("Program compiled succesfully!")
            return output

    def build():
        if mainwindow.build_loc is None or '':
            mainwindow.build_as()
        else:
            with open(mainwindow.build_loc, "wb") as f:
                file_str = mainwindow.compile()
                file_b = Linker.link(file_str)
                f.write(file_b)
                mainwindow.build = True


    def build_as():
        mainwindow.build_loc,_ = QFileDialog.getSaveFileName(window,
            "Build file", "", "Kholisa32 runtime file (*.khr)")

        mainwindow.build_name = mainwindow.build_loc.rsplit('/', 1)[-1]

        with open(mainwindow.build_loc, "wb") as f:
            file_str = mainwindow.compile()
            file_b = Linker.link(file_str)
            f.write(file_b)
            mainwindow.build = True

    def upload():
        open_loc,_ = QFileDialog.getOpenFileName(window, "Open file", "", "Kholisa32 runtime file (*.khr)")

        with open(open_loc, "rb") as f:
            if Uart.transfer_binary(f.read()):
                window.buildLog.setText("Error during transmission!\n")

    def build_and_upload():
        mainwindow.build()
        with open(mainwindow.build_loc, "rb") as f:
            Uart.transfer_binary(f.read())

    def new():
        if mainwindow.saved == False:
            msgBox = QMessageBox(QMessageBox.Question, "Save", "Save file?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Yes)

            ans = msgBox.exec_()

            if ans == QMessageBox.Yes:
                mainwindow.save()
            elif ans == QMessageBox.No:
                pass
            elif ans == QMessageBox.Cancel:
                return
            else:
                return

        mainwindow.save_loc = None;
        window.editor.setPlainText(None)
        window.editor_tab.tabBar().setTabTextColor(window.editor_tab.currentIndex(), QColor("black"))
        mainwindow.saved = True

    def open():
        open_loc,_ = QFileDialog.getOpenFileName(window,
            "Open file", "", "Kholisa32 assembly file (*.khl)")

        mainwindow.save_loc = open_loc
        mainwindow.save_name = mainwindow.save_loc.rsplit('/', 1)[-1]

        with open(open_loc, "r") as f:
            window.editor.setPlainText(f.read())
            window.editor_tab.setTabText(window.editor_tab.currentIndex(), mainwindow.save_name);
            window.editor_tab.tabBar().setTabTextColor(window.editor_tab.currentIndex(), QColor("black"))
            mainwindow.saved = True

    def save():
        if mainwindow.save_loc is None or '':
            mainwindow.save_as()
        else:
            with open(mainwindow.save_loc, "w") as f:
                f.write(window.editor.toPlainText())
                mainwindow.saved = True
                window.editor_tab.tabBar().setTabTextColor(window.editor_tab.currentIndex(), QColor("black"))

    def save_as():
        mainwindow.save_loc,_ = QFileDialog.getSaveFileName(window,
            "Save file", "", "Kholisa32 assembly file (*.khl)")

        mainwindow.save_name = mainwindow.save_loc.rsplit('/', 1)[-1]

        with open(mainwindow.save_loc, "w") as f:
            f.write(window.editor.toPlainText())
            mainwindow.saved = True
            window.editor_tab.tabBar().setTabTextColor(window.editor_tab.currentIndex(), QColor("black"))

        window.editor_tab.setTabText(window.editor_tab.currentIndex(), mainwindow.save_name);

    def generate_preset():
        window.editor.setPlainText(
        ".name = '"'name'"'\n"  \
        "\n"                    \
        ".icon = \n"            \
        "\n"                    \
        ".img = {\n"            \
        "   \n"                 \
        "}\n"                   \
        "\n "                   \
        ".sound = {\n"          \
        "   \n"                 \
        "}\n"                   \
        "\n"                    \
        "init:\n"               \
        "   \n"                 \
        "main:\n"               \
        "   \n"                 \
        "    jmp main\n"
        )

    def add_icon():
        doc = window.editor.toPlainText().split("\n")
        cursor =  window.editor.textCursor()
        mode = 0


        icon_loc,_ = QFileDialog.getOpenFileName(window,
            "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        for (line, text) in enumerate(doc):
            if ".icon" in text:
                mode += 2
                i_loc = line
            elif ".name" in text:
                mode += 1
                n_loc = line

        if mode >= 2:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  i_loc)
            cursor.movePosition(cursor.Right, cursor.MoveAnchor,  7)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText(" " + icon_loc + " \n")

        elif mode == 1:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  n_loc+1)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText("\n.icon = " + icon_loc + " ")

        else:
            cursor.setPosition(0);
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText("\n.icon = " + icon_loc + " ")

    def add_image():
        doc = window.editor.toPlainText().split("\n")
        cursor =  window.editor.textCursor()
        mode = 0


        image_loc,_ = QFileDialog.getOpenFileNames(window,
            "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        for (line, text) in enumerate(doc):
            if ".img" in text:
                mode += 2
                i_loc = line
            elif ".name" in text:
                mode += 1
                n_loc = line

        if mode >= 2:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  i_loc+1)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText("\t" + "\n\t".join(image_loc) + " \n")

        elif mode == 1:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  n_loc+1)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText(
            "\n"                    \
            ".img = {\n"            \
            "\t%s\n"                \
            "}\n"                   \
            "\n" % ("\n\t".join(image_loc))
            )

        else:
            cursor.setPosition(0);
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText(
            "\n"                    \
            ".img = {\n"            \
            "\t%s\n"                \
            "}\n"                   \
            "\n" % ("\n\t".join(image_loc))
            )

    def add_sound():
        doc = window.editor.toPlainText().split("\n")
        cursor =  window.editor.textCursor()
        mode = 0


        sound_loc,_ = QFileDialog.getOpenFileNames(window,
            "Open Sound File", "", "WAV Files (*.wav)")

        for (line, text) in enumerate(doc):
            if ".sound" in text:
                mode += 2
                i_loc = line
            elif ".name" in text:
                mode += 1
                n_loc = line

        if mode >= 2:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  i_loc+1)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText("\t" + "\n\t".join(sound_loc) + " \n")

        elif mode == 1:
            cursor.setPosition(0);
            cursor.movePosition(cursor.Down, cursor.MoveAnchor,  n_loc+1)
            window.editor.setTextCursor(cursor)

            window.editor.insertPlainText(
            "\n"                    \
            ".sound = {\n"          \
            "\t%s\n"                \
            "}\n"                   \
            "\n" % ("\n\t".join(sound_loc))
            )

        else:
            cursor.setPosition(0);
            window.editor.setTextCursor(cursor)

            """ TBI """
            window.editor.insertPlainText(
            "\n"                    \
            ".sound = {\n"          \
            "\t%s\n"                \
            "}\n"                   \
            "\n" % ("\n\t".join(sound_loc))
            )

    def text_changed():
        mainwindow.saved = False
        window.editor_tab.tabBar().setTabTextColor(window.editor_tab.currentIndex(), QColor("red"))

    def cursor_pos_changed():
        cursorX = window.editor.textCursor().columnNumber()+1
        cursorY = window.editor.textCursor().blockNumber()+1
        window.labelCursorPos.setText(f"Ln = {cursorY}, Col = {cursorX}")


    def set_port(port: str):
        Uart.set_port(port)
        window.labelPort.setText("Port="+port)

    def set_baud(baud: int):
        Uart.set_baudrate(baud)
        window.labelBaud.setText("Baud={}".format(baud))



if __name__ == "__main__":
    print("Application started!")
    app = QApplication([])

    ui_file = QFile("mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)

    mainwindow.init()
    Uart.init()

    """ Shape menu """
    window.menuPort = QMenu("&Port")
    window.menuOptions.addMenu(window.menuPort)

    actionsPort: list = []

    for port in Uart.get_port_names():
        tmp = QAction(port)
        window.menuPort.addAction(tmp)
        tmp.setMenuRole(QAction.TextHeuristicRole)
        tmp.triggered.connect(lambda _=None, text=port: mainwindow.set_port(text))
        actionsPort.append(tmp)

    window.menuBaud = QMenu("&Baud")
    window.menuOptions.addMenu(window.menuBaud)

    actionsBaud = []
    for baud in [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]:
        tmp = QAction(str(baud))
        window.menuBaud.addAction(tmp)
        tmp.setMenuRole(QAction.TextHeuristicRole)
        tmp.triggered.connect(lambda _=None, val=baud: mainwindow.set_baud(val))
        actionsBaud.append(tmp)


    """ Set footer """
    window.labelPort.setText("Port="+Uart.port)
    window.labelBaud.setText("Baud={}".format(Uart.baud))


    """ Connects """
    window.actionBuild.triggered.connect(mainwindow.build)
    window.actionBuild_as.triggered.connect(mainwindow.build_as)
    window.actionBuild_and_upload.triggered.connect(mainwindow.build_and_upload)
    window.actionUpload.triggered.connect(mainwindow.upload)

    window.actionGenerate_preset.triggered.connect(mainwindow.generate_preset)
    window.actionAdd_image.triggered.connect(mainwindow.add_image)
    window.actionSet_icon.triggered.connect(mainwindow.add_icon)
    window.actionAdd_WAV.triggered.connect(mainwindow.add_sound)

    window.actionNew.triggered.connect(mainwindow.new)
    window.actionOpen.triggered.connect(mainwindow.open)
    window.actionSave.triggered.connect(mainwindow.save)
    window.actionSave_as.triggered.connect(mainwindow.save_as)

    window.editor.textChanged.connect(mainwindow.text_changed)
    window.editor.cursorPositionChanged.connect(mainwindow.cursor_pos_changed)

    app.aboutToQuit.connect(mainwindow.exit)

    window.show()
    sys.exit(app.exec_())
