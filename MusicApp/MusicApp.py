import os
import sys
import wave
import random
import pygame
from mutagen.mp3 import MP3
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
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


Config.set('graphics','resizable', False)

music_path = "./musics/"

class ImageButton(ButtonBehavior, Image):
	pass

class Song:

	def time(self, time):
		res = ""
		if time < 3600:
			res = str(time // 60)+'.'+str(time % 60)
		else:
			res = str(time // 3600)+'.'+str((time % 3600) // 60)+'.'+str((time % 3600) % 60)
		return res

	def length(self, src):
		audio = MP3(src)
		duration = int(audio.info.length)
		return self.time(duration)


class MainScreen(GridLayout):

	def __init__(self,**kwargs):
		super(GridLayout, self).__init__(**kwargs)
		pygame.init()
		pygame.mixer.init()
		self.first_song = True
		if os.path.exists(music_path):
			self.all_songs = os.listdir(music_path)
		else:
			sys.exit()
		self.song = self.ids.song
		self.play = self.ids.play

		if self.first_song:
			current_song = random.choice(self.all_songs)
			self.song.text = current_song

		dur = Song().length(music_path+'/'+self.song.text)
		self.ids.duration.text = "0.00/"+dur
		self.ids.progress.max = 60*dur.split('.')[0] + dur.split('.')[1]


	def update(self, dt):
		current_time = Song().time(int(pygame.mixer.music.get_pos()/1000))
		self.ids.duration.text = current_time+'/'+self.ids.duration.text.split('/')[1]
		self.ids.progress.value = current_time

	def next_song(self):
		self.song.text = "Next song"

	def previous_song(self):
		self.song.text = "Previous song"

	def on_play(self):
		if self.play.source.split('/')[1] == "play.png":

			if self.play.started:
				pygame.mixer.music.unpause()
			else:
				pygame.mixer.music.load(music_path+self.song.text)
				pygame.mixer.music.play()
				self.play.started = 1
			self.play.source = self.play.source.split('/')[0]+"/stop.png"
			Clock.schedule_interval(self.update, 0.5)
		else:
			pygame.mixer.music.pause()
			self.play.source = self.play.source.split('/')[0]+"/play.png"
			Clock.unschedule(self.update)


class MusicApp(App):

	def build(self):
		Window.size = (400, 100)
		self.title = "Music Player"
		return MainScreen()


if __name__ == '__main__':
    MusicApp().run()
