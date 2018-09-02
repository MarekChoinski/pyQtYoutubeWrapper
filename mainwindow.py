import sys
from os.path import expanduser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView

import youtube_dl as yt
import pprint
import urllib.request

from downloader import Downloader
from video import Video

from listitem import ListItem
from ui_mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # this variables declares which state should be setted by check_all-button
        self.checked_all = False

        # thread
        self.thread = None
        self.downloader = None

        # videos
        self.videos = []

        # slots
        self.ui.addButton.clicked.connect(self.search)
        self.ui.downloadButton.clicked.connect(self.download)
        self.ui.checkAllButton.clicked.connect(self.check_all)
        self.ui.cleanButton.clicked.connect(self.clean_list)

        self.ui.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.mp3_options = {
            'format': 'bestaudio',  # 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # 192',
            }],
            'logger': MainWindow.MyLogger(),
            'progress_hooks': [self.my_hook],
        }

        # TODO test
        # self.ui.searchLineEdit.setText(
        #    "https://www.youtube.com/watch?v=8GW6sLrK40k&list=PLit8GzUQ7d7F0Lf2WNNL754TYQHb23b8t&t=0s&index=2")
        self.ui.searchLineEdit.setText(
            "https://www.youtube.com/watch?v=kfchvCyHmsc")
        # TODO test
        self.search()

    class MyLogger:
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    @pyqtSlot()
    def search(self):
        # TODO so bad it is very slow, but it is youtube-dl problem
        with yt.YoutubeDL(self.mp3_options) as ydl:
            result = ydl.extract_info(
                self.ui.searchLineEdit.text(),
                download=False  # We just want to extract the info
            )

        self.update_list(result)

    @pyqtSlot()
    def download(self):

        # path = QtWidgets.QFileDialog.getExistingDirectory(
        #     self,
        #     "Otwórz",
        #     expanduser("~"),
        #     QtWidgets.QFileDialog.ShowDirsOnly
        # )

        # TODO test
        path = '/home/marek/Desktop'

        if path and self.videos:
            self.thread = QThread()
            self.downloader = Downloader(path, self.videos, self.mp3_options)

            self.downloader.moveToThread(self.thread)
            self.thread.started.connect(self.downloader.download)
            self.download_is_running(True)
            self.downloader.finished.connect(lambda: self.download_is_running(False))

            self.thread.start()

    def update_list(self, videos):

        if 'entries' in videos:
            for video in videos['entries']:
                if video['title'] not in (v.original_title for v in self.videos):
                    record = Video(video['url'],
                                   video['title'],
                                   video['duration'],
                                   video['thumbnail'])
                    record.is_checked = True
                    self.videos.append(record)

        else:

            if videos['title'] not in (v.original_title for v in self.videos):
                record = Video(videos['url'],
                               videos['title'],
                               videos['duration'],
                               videos['thumbnail'])
                record.is_checked = True
                self.videos.append(record)

        self.show_list()

    @pyqtSlot()
    def check_all(self):

        for v in self.videos:
            v.is_checked = not self.checked_all

        self.checked_all = not self.checked_all

        text = 'Odznacz' if self.checked else 'Zaznacz'
        self.ui.checkAllButton.setText(text)

    def show_list(self):

        self.ui.listWidget.clear()

        for video in self.videos:
            # create an item
            Item = QtWidgets.QListWidgetItem(self.ui.listWidget)
            # create a custom widget
            Item_Widget = ListItem()

            # set thumbnail
            url = video.thumbnail
            data = urllib.request.urlopen(url).read()

            image = QtGui.QImage()
            image.loadFromData(data)
            image = image.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
            Item_Widget.setPixmap(QtGui.QPixmap(image))

            Item_Widget.setTitle(video.title)
            Item_Widget.setDuration(video.duration)

            Item_Widget.setChecked(video.is_checked)
            # self.checkboxes.append(Item_Widget.getCheckBox())

            # set the size from the item to the same of the widget
            Item.setSizeHint(Item_Widget.sizeHint())
            # Item.setFlags(Item.flags() | QtCore.Qt.ItemIsSelectable)  # TODO not working
            # Item.
            # I add it to the list
            self.ui.listWidget.addItem(Item)
            # self.items.append(Item)
            video.checkbox = Item_Widget.getCheckBox()
            video.line_edit = Item_Widget.getLineEdit()

            self.ui.listWidget.setItemWidget(Item, Item_Widget)

    @pyqtSlot()
    def clean_list(self):

        self.videos = []
        self.items = []
        self.checkboxes = []
        self.checked = False
        self.show_list()

    def download_is_running(self, is_running):
        self.ui.downloadButton.setEnabled(not is_running)

        if self.thread:
            self.thread.exit()

        # if not is_running:
        #     del self.thread
        #     self.thread = None
        #     del self.downloader
        #     self.downloader = None
