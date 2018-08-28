class Video:
    def __init__(self, url, title, duration, thumbnail):
        self.url = url
        self.original_title = title
        self.duration = duration
        self.thumbnail = thumbnail

        self.checkbox = None
        self.line_edit = None

    @property
    def title(self):
        if self.line_edit:
            return self.line_edit.text()
        else:
            return self.original_title

    def is_checked(self):
        return True#self.checkbox.isChecked()
