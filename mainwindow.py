import sys
from os.path import expanduser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QApplication

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

        # checkboxes
        self.checked = True
        self.checkboxes = []

        # items
        self.items = []

        # videos
        self.videos = []

        # slots
        self.ui.addButton.clicked.connect(self.search)
        self.ui.downloadButton.clicked.connect(self.download)
        self.ui.checkAllButton.clicked.connect(self.check_all)
        self.ui.cleanButton.clicked.connect(self.clean_list)

        # youtube-dl
        # self.ydl = yt.YoutubeDL()

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
        self.ui.searchLineEdit.setText(
            "https://www.youtube.com/watch?v=8GW6sLrK40k&list=PLit8GzUQ7d7F0Lf2WNNL754TYQHb23b8t&t=0s&index=2")
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

    def search(self):
        # TODO so bad it is very slow, but it is youtube-dl problem
        with yt.YoutubeDL(self.mp3_options) as ydl:
            result = ydl.extract_info(
                self.ui.searchLineEdit.text(),
                download=False  # We just want to extract the info
            )

        self.update_list(result)

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
            self.ddd = Downloader(path, self.videos, self.mp3_options)

            self.ddd.moveToThread(self.thread)
            self.thread.started.connect(self.ddd.download)
            self.download_is_running(True)
            self.thread.finished.connect(lambda: self.download_is_running(False))

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

    def check_all(self):

        for checkbox in (x.checkbox for x in self.videos):
            checkbox.setChecked(not self.checked)

        self.checked = not self.checked

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
            Item.setFlags(Item.flags() | QtCore.Qt.ItemIsSelectable)  # TODO not working
            # I add it to the list
            self.ui.listWidget.addItem(Item)
            # self.items.append(Item)
            # video.checkbox = Item.getCheckBox()
            # video.line_edit = Item.getLineEdit()

            self.ui.listWidget.setItemWidget(Item, Item_Widget)

    def clean_list(self):

        self.videos = []
        self.items = []
        self.checkboxes = []
        self.checked = False
        self.show_list()

    def update_titles(self):
        for v in self.videos:
            v.title = v.line_edit.text()

    def download_is_running(self, is_running):
        self.ui.downloadButton.setEnabled(not is_running)
