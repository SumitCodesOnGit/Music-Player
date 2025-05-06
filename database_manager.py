import sqlite3

class DataBaseManager:

    def __init__(self, db_name="music.db"):
        self.conn = sqlite3.connect("db_name")
        self.create_tables()


    def create_tables(self):
        query1 = """
        CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        album_id TEXT,
        file_path TEXT NOT NULL,
        duration TEXT,
        FOREIGN KEY(album_id) REFERENCES albums(id)
                  ) """
        
        self.conn.execute(query1)

        query2 = """
        CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        artist TEXT,
        year TEXT,
        genre TEXT)       """

        self.conn.execute(query2)

        self.conn.commit()



    def add_album(self, name, artist, year, genre):
        self.conn.execute("INSERT INTO albums (name, artist, year, genre) VALUES (?,?,?,?)", (name, artist, year, genre))
        self.conn.commit()


    def get_all_albums(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from albums")
        return cursor.fetchall()
    

    def get_album_id(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM albums WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    

    def get_songs_by_album_id(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM songs where album_id=?", (album_id,))
        return cursor.fetchall()


    def add_song(self, song_data):
        query = "INSERT INTO songs (title, artist, album_id, file_path, duration) values (?,?,?,?,?)"
        self.conn.execute(query,song_data)
        self.conn.commit()


    def get_all_songs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()
    

    def delete_album(self, album_id):
        self.conn.execute("DELETE FROM songs WHERE album_id = ?",(album_id,))
        self.conn.execute("DELETE FROM albums WHERE id = ?", (album_id,))
        self.conn.commit()


    def rename_album(self, album_id, new_name):
        query = "UPDATE albums SET name = ? WHERE id = ?"
        self.conn.execute(query,(new_name, album_id))
        self.conn.commit()


