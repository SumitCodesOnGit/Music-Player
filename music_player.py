import pygame
import os

class MusicPlayer:

    def __init__(self):
        pygame.mixer.init()   # initializes the mixer module 
        self.current_song_path = None # stores the currently playing song's file path


    def play(self, song_path):  
        """ plays the song at the specified path"""  
        if os.path.exists(song_path):
            pygame.mixer.music.load(song_path)   # loads the song file into the mixer
            pygame.mixer.music.play()            # starts playback
            self.current_song_path = song_path   # stores the path of current song


    def pause(self):
        pygame.mixer.music.pause()


    
    def resume(self):
        pygame.mixer.music.unpause()


    
    def stop(self):
        pygame.mixer.music.stop()


        
    


