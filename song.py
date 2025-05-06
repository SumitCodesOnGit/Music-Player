
class Song:

    def __init__(self, id, title, artist, album, file_path, duration):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.file_path = file_path
        self.duration = duration


    def __str__(self):
        return f"{self.title} by {self.artist}"