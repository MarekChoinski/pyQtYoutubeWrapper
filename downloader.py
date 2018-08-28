from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import youtube_dl as yt


class Downloader(QObject):
    # Create the signal
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    def __init__(self, path, videos, options, parent=None):
        super(Downloader, self).__init__(parent)

        self.path = path
        self.videos = videos
        self.options = options

        # Connect signal to the desired function
        # self.sig.connect(updateProgBar)

    @pyqtSlot()
    def download(self):

        for video in self.videos:
            if True:  # checkbox
                print(video.url, " !! ")

                self.options['outtmpl'] = self.path + '/' + video.title + '.%(ext)s'

                with yt.YoutubeDL(self.options) as ydl:
                    ydl.download([video.url])
