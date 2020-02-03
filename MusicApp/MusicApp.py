import os
import pygame
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty


Config.set('graphics','resizable', False)

music_path = "./musics/"

class ImageButton(ButtonBehavior, Image):
	pass

class MainScreen(GridLayout):

	def __init__(self,**kwargs):
		super(GridLayout, self).__init__(**kwargs)
		pygame.init()
		pygame.mixer.init()
		self.first_song = True
		self.all_songs = os.listdir(music_path)
		self.song = self.ids.song
		self.play = self.ids.play

	def next_song(self):
		self.song.text = "Next song"

	def previous_song(self):
		self.song.text = "Previous song"


	def on_play(self):
		if self.play.source.split('/')[1] == "play.png":
			if self.first_song:
				current_song = random.choice(self.all_songs)
				self.song.text = current_song
			else:
				self.song.text = "Play song"

			if self.play.started:
				pygame.mixer.music.unpause()
			else:
				pygame.mixer.music.load(music_path+self.song.text)
				pygame.mixer.music.play()
				self.play.started = 1
			self.play.source = self.play.source.split('/')[0]+"/stop.png"
		else:
			pygame.mixer.music.pause()

			self.play.source = self.play.source.split('/')[0]+"/play.png"


class MusicApp(App):

	def build(self):
		Window.size = (400, 100)
		self.title = "Music Player"
		return MainScreen()


if __name__ == '__main__':
    MusicApp().run()
