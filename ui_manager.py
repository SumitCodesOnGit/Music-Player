import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from database_manager import DataBaseManager
from music_player import MusicPlayer
from album import Album
from song import Song
import os

class UIManager:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Music Player")

        # Set theme and style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=('Helvetica',10))
        style.configure("TLabel", font=('Helvetica',11,'bold'))

        self.db = DataBaseManager()
        self.player = MusicPlayer()

        ttk.Label(root, text="Advanced Music Player", font=('Helvetica',14,'bold')).pack(pady=10)

        # left panel
        album_frame = tk.Frame(root, padx=10, pady=10)
        album_frame.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(album_frame, text="Albums").pack(anchor='w')

        self.album_listbox = tk.Listbox(album_frame, width=30, font=('Helvetica',10))
        self.album_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.album_listbox.bind("<<ListboxSelect>>",self.on_album_select)
        
        # middle panel
        song_frame = tk.Frame(root, padx=10, pady=10)
        song_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(song_frame, text="Songs").pack(anchor='w')

        self.song_listbox = tk.Listbox(song_frame, width=50, font=('Helvetica',10))
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        

        # Right panle (controls)

        button_frame = tk.Frame(root, padx=10, pady=10)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(button_frame, text="Play", command=self.play_selected).pack(pady=5)
        ttk.Button(button_frame, text="Pause", command=self.player.pause).pack(pady=5)
        ttk.Button(button_frame, text="Resume", command=self.player.resume).pack(pady=5)
        ttk.Button(button_frame, text="Stop", command=self.player.stop).pack(pady=5)
        ttk.Button(button_frame, text="Add Album", command=self.add_album).pack(pady=5)
        ttk.Button(button_frame, text="Add Song", command=self.add_song).pack(pady=5)
        
        # rename and delete buttons
        ttk.Button(button_frame, text="Rename Album", command=self.rename_album).pack(pady=5)
        ttk.Button(button_frame, text="Delete Album", command=self.delete_album).pack(pady=5)

        self.albums = []
        self.songs = []

        self.load_albums()



    def load_albums(self):
        self.albums = self.db.get_all_albums()
        self.album_listbox.delete(0, tk.END)
        for album in self.albums:
            self.album_listbox.insert(tk.END, f"{album[1]}")


    def on_album_select(self,event):
        selection = self.album_listbox.curselection()
        if selection:
            album_id = self.albums[selection[0]][0]
            self.songs = self.db.get_songs_by_album_id(album_id)
            self.song_listbox.delete(0, tk.END)
            for song in self.songs:
                self.song_listbox.insert(tk.END, f"{song[1]} - {song[2]}")


    def play_selected(self):
        index = self.song_listbox.curselection()
        if index:
            song = self.songs[index[0]]
            self.player.play(song[4])


    def add_album(self):
        name =  simpledialog.askstring("Album Name", "Enter Album Name: ")
        if not name:
            return
        artist =  simpledialog.askstring("Artist","Enter Artist Name: ")
        if not artist:
            return
        year = simpledialog.askstring("Year", "Enter Year: ")
        if year is None:
            year = ""
        genre = simpledialog.askstring("Genre", "Enter Genre: ")
        if genre is None:
            genre = ""
        
        self.db.add_album(name, artist, year, genre)
        self.load_albums()



    def add_song(self):
        selection = self.album_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Album Selected", "please select an album to add the song to.")
            return
        
        album_id = self.albums[selection[0]][0]
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            title = os.path.basename(file_path)
            try:
                self.db.add_song((title, "Unknown", album_id, file_path, "Unknown"))
                self.on_album_select(None)
            except Exception as e:
                messagebox.showerror("Error", str(e))



    
    def rename_album(self):
        selection = self.album_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an album to rename.")
            return
        
        album = self.albums[selection[0]]
        album_id = album[0]
        print("Rename function triggered")   # for debug
        print(f"Selected album ID and name:  {album[0]}  {album[1]} by {album[2]}")
        new_name = simpledialog.askstring("Rename Album",f"Enter new name for {album[1]}: ")
        if new_name and new_name.strip():
            try:
                self.db.rename_album(album[0], new_name.strip())
                print("Renamed to: ", new_name) # for debug
                self.load_albums()
            except Exception as e:
                messagebox.showerror("Rename Error", str(e))
        else:
            print("No new name entered.") # Debug line


    def delete_album(self):
        selection = self.album_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection","Select an album to delete.")
            return
        
        album = self.albums[selection[0]]
        confirm = messagebox.askyesno("Confirm Delete",f"Delete album {album[1]} and its songs?")
        if confirm:
            self.db.delete_album(album[0])
            self.load_albums()
            self.song_listbox.delete(0, tk.END)





            




