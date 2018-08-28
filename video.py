class Video:
    def __init__(self, url, title, duration, thumbnail):
        self.url = url
        self.title = title
        self.original_title = title
        self.duration = duration
        self.thumbnail = thumbnail

        self.checkbox = None
        self.line_edit = None
        self.is_checked = True
