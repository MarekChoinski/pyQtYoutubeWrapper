from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import youtube_dl as yt


class Downloader(QObject):
    # Create the signal

    finished = pyqtSignal()
    error_occured = pyqtSignal(str)

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
            if video.checkbox.isChecked():

                try:
                    self.options['outtmpl'] = f'{self.path}/{video.title}.webm' #%(ext)s'

                    with yt.YoutubeDL(self.options) as ydl:
                        ydl.download([video.url])
                except yt.DownloadError:
                    self.error_occured.emit(f'Problem occured with "{video.original_title}".\nCheck connection.')


        self.finished.emit()
        del self
