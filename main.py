import pyperclip
from PySide6 import QtCore, QtGui, QtWidgets

from PySide6.QtCore import Qt
from pynput import keyboard

import argparse
import sys
import pytesseract

from logger import log_copied, log_ocr_failure
from notifications import notify_copied, notify_ocr_failure
from ocr import ensure_tesseract_installed, get_ocr_result


class Snipper(QtWidgets.QWidget):
    def __init__(self, parent, langs=None, flags=Qt.WindowFlags()):
        super().__init__()

        self.setWindowTitle("Txt Scribe")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()
        self.langs = langs

    def getWindow(self):
        return self._screen.grabWindow(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # escape to quit without snipping
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.globalPosition().toPoint()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.globalPosition().toPoint()
        self.update()
        return super().mousePressEvent(event)

    def snipOcr(self):
        self.hide()

        ocr_result = self.ocrOfDrawnRectangle()
        if ocr_result:
            return ocr_result
        else:
            log_ocr_failure()

    def hide(self):
        super().hide()
        QtWidgets.QApplication.processEvents()

    def ocrOfDrawnRectangle(self):
        return get_ocr_result(
            self.getWindow().copy(
                min(self.start.x(), self.end.x()),
                min(self.start.y(), self.end.y()),
                abs(self.start.x() - self.end.x()),
                abs(self.start.y() - self.end.y()),
            ),
            self.langs,
        )


class OneTimeSnipper(Snipper):
    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        ocr_result = self.snipOcr()
        if ocr_result:
            pyperclip.copy(ocr_result)
            # log_copied(ocr_result)
            notify_copied(ocr_result)
        else:
            notify_ocr_failure()

        QtWidgets.QApplication.quit()


arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument(
    "langs",
    nargs="?",
    default="eng",
    help='languages passed to tesseract, eg. "eng+fra" (default: %(default)s)',
)


def take_textshot(langs):
    pytesseract.pytesseract.tesseract_cmd = (
        "D:/Tesseract/tesseract.exe"  # your path may be different
    )

    ensure_tesseract_installed()

    # QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)

    # Checking if QApplication already exists
    if not QtWidgets.QApplication.instance():  # If it doesn't exist
        app = QtWidgets.QApplication(sys.argv)

    else:
        # If it does exist, use the existing instance
        app = QtWidgets.QApplication.instance()

    window = QtWidgets.QMainWindow()

    # Hide the previous snipper, if any
    if hasattr(take_textshot, "snipper"):
        take_textshot.snipper.hide()

    snipper = OneTimeSnipper(window, langs)
    snipper.show()

    sys.exit(app.exec())


def shortcut():
    args = arg_parser.parse_args()
    take_textshot(args.langs)


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<alt>+g"), shortcut)  # hotkey
with keyboard.Listener(
    on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)
) as listener:
    listener.join()


def main():
    shortcut()


if __name__ == "__main__":
    main()
