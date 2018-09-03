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
        self.setWindowTitle("Youtube downloader")

        self.checked_all = False  # declares which state should be setted by check_all-button

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

        # ui
        self.ui.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.ui.mp3CheckBox.setChecked(True)
        self.ui.labelInformation.setVisible(False)
        self.ui.progressBarSingle.setVisible(False)
        self.ui.progressBarMultiple.setVisible(False)

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

        # TODO don't work video downloading
        # self.video_options = {
        #     'format': 'bestvideo+bestaudio',
        #     'noplaylist': True,
        #     # 'ext': '3gp',  # 'bestaudio/best',
        #     'logger': MainWindow.MyLogger(),
        #     'progress_hooks': [self.my_hook],
        # }

        # TODO test
        # self.ui.searchLineEdit.setText(
        #    "https://www.youtube.com/watch?v=8GW6sLrK40k&list=PLit8GzUQ7d7F0Lf2WNNL754TYQHb23b8t&t=0s&index=2")
        self.ui.searchLineEdit.setText(
            "https://www.youtube.com/watch?v=kfchvCyHmsc")
        # TODO test
        self.search()

    class MyLogger:  # TODO
        def debug(self, msg):
            print(msg)

        def warning(self, msg):
            print(msg)

        def error(self, msg):
            print(msg)

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    @pyqtSlot()
    def search(self):


        self.ui.labelInformation.setVisible(False)

        if self.ui.searchLineEdit.text():
            try:
                # TODO so bad it is very slow, but this is a youtube-dl problem
                with yt.YoutubeDL(self.get_options()) as ydl:
                    result = ydl.extract_info(
                        self.ui.searchLineEdit.text(),
                        download=False  # We just want to extract the info
                    )

                # TODO test
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(result)

                self.update_list(result)
            except yt.DownloadError:
                self.print_error("Download is not possible.\nCheck you internet connection or link.")

    @pyqtSlot()
    def download(self):



        self.ui.labelInformation.setVisible(False)

        if self.videos:
            try:
                # TODO test
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
                    self.downloader = Downloader(path, self.videos, self.get_options())

                    self.downloader.moveToThread(self.thread)
                    self.thread.started.connect(self.downloader.download)
                    self.download_is_running(True)
                    self.downloader.finished.connect(lambda: self.download_is_running(False))
                    self.downloader.error_occured.connect(self.print_error)

                    self.thread.start()

            except yt.DownloadError:
                self.print_error("Download is not possible.\nCheck you internet connection or link.")


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


        self.ui.labelInformation.setVisible(False)

        if self.videos:
            for v in self.videos:
                v.is_checked = not self.checked_all

            self.checked_all = not self.checked_all

            text = 'Odznacz' if self.checked_all else 'Zaznacz'
            self.ui.checkAllButton.setText(text)

    def show_list(self):

        self.ui.listWidget.clear()

        for video in self.videos:
            # create an item
            item = QtWidgets.QListWidgetItem(self.ui.listWidget)
            # create a custom widget
            item_widget = ListItem()

            # set thumbnail
            url = video.thumbnail
            data = urllib.request.urlopen(url).read()

            image = QtGui.QImage()
            image.loadFromData(data)
            image = image.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
            item_widget.setPixmap(QtGui.QPixmap(image))

            item_widget.setTitle(video.title)
            item_widget.setDuration(video.duration)

            item_widget.setChecked(video.is_checked)
            # self.checkboxes.append(Item_Widget.getCheckBox())

            # set the size from the item to the same of the widget
            item.setSizeHint(item_widget.sizeHint())
            # Item.setFlags(Item.flags() | QtCore.Qt.ItemIsSelectable)  # TODO not working
            # Item.
            # I add it to the list
            self.ui.listWidget.addItem(item)
            # self.items.append(Item)
            video.checkbox = item_widget.getCheckBox()
            video.line_edit = item_widget.getLineEdit()

            self.ui.listWidget.setItemWidget(item, item_widget)

    @pyqtSlot()
    def clean_list(self):

        self.videos = []
        self.checked_all = False
        self.ui.labelInformation.setVisible(False)
        self.show_list()

    def download_is_running(self, is_running):
        self.ui.downloadButton.setEnabled(not is_running)

        if self.thread:
            self.thread.exit()

    def get_options(self):
        if self.ui.mp3CheckBox.isChecked():
            return self.mp3_options
        else:
            return self.video_options

    @pyqtSlot(str)
    def print_error(self, msg):
        self.ui.labelInformation.setVisible(True)
        self.ui.labelInformation.setText(msg)
