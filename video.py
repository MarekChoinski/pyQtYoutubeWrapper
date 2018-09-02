class Video:
    def __init__(self, url, title, duration, thumbnail):
        self.url = url
        self.original_title = title
        self.duration = duration
        self.thumbnail = thumbnail
        self._is_checked = None

        self.checkbox = None
        self.line_edit = None

    @property
    def title(self):
        if self.line_edit:
            return self.line_edit.text()
        else:
            return self.original_title

    @property
    def is_checked(self):
        if self.checkbox:
            return self.checkbox.isChecked()
        else:
            return self._is_checked

    @is_checked.setter
    def is_checked(self, value):
        self._is_checked = value
        if self.checkbox:
            self.checkbox.setChecked(value)

