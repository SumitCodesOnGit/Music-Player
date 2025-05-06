
class Album:

    """ Organize and group song objects under a shared album"""

    def __init__(self, name, artist, year=None, genre=None):
        self.name = name
        self.artist = artist
        self.year = year
        self.genre = genre
        self.songs = []


    def add_song(self, song):
        self.songsa.append(song)



    def get_song_list(self):
        return [str(song) for song in self.songs]
    


    def __str__(self):
        return f"{self.name} by {self.artist}"