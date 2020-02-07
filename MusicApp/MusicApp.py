import os
import sys
import wave
import random
from pygame.mixer import init
from pygame.mixer import music
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
			res = str(time // 60)+'.'+self.format_seconds(str(time % 60))
		else:
			res = str(time // 3600)+'.'+self.format_seconds(str(time % 3600)) // 60+'.'+self.format_seconds(str(time % 3600)) % 60
		return res


	def format_seconds(self, sec):
		res = sec
		if int(sec) < 10:
				res = '0'+sec
		return res


	def length(self, src):
		audio = MP3(src)
		duration = int(audio.info.length)
		return self.time(duration)


class MainScreen(GridLayout):

	def __init__(self,**kwargs):

		super(GridLayout, self).__init__(**kwargs)
		init()

		self.first_song = True
		self.randomSongs = True

		self.pressed_back = 0
		# This variable stands
		self.last_songs = []
		# This will store the last 20 songs listened

		if os.path.exists(music_path):
			self.all_songs = os.listdir(music_path)
		else:
			sys.exit()
		self.song = self.ids.song
		self.play = self.ids.play

		if self.last_songs == []:
			current_song = random.choice(self.all_songs)
			self.song.text = current_song

		self.initSong(self.song.text)

		# It will used to control the volume and all the icon related to it
		#Clock.schedule_interval(self.check_volume, 0.1)


	def initSong(self,name):
		dur = Song().length(music_path+'/'+name)
		self.ids.duration.text = "0.00/"+dur
		self.ids.progress.max = 60*int(dur.split('.')[0]) + int(dur.split('.')[1])


	def update(self, dt):
		pos = music.get_pos() / 1000
		"""
		if int(pos) != self.ids.progress.value and int(10*round((music.get_pos()/1000)%1,2)) >= 1:
			music.rewind()
			music.set_pos(self.ids.progress.value)
			print("Hello: "+str(self.ids.progress.value)+' - '+str(music.get_pos()))
		"""
		current_time = Song().time(int(pos))
		self.ids.duration.text = current_time+'/'+self.ids.duration.text.split('/')[1]
		self.ids.progress.value = 60*int(current_time.split('.')[0]) + int(current_time.split('.')[1])



	def next_song(self):
		print(self.last_songs)
		self.play.started = 0
		if self.pressed_back != 0:
			self.pressed_back -= 1
			self.song.text = self.last_songs[-self.pressed_back]
		else:
			if self.randomSongs:
				differentSong = False
				while not differentSong:
					nextSong = random.choice(self.all_songs)
					if self.song.text is not nextSong:
						differentSong = True
						self.last_songs.append(self.song.text)
						self.song.text = nextSong
			else:
				self.last_songs.append(self.song.text)
				if self.song.text == self.all_songs[-1]:
					self.song.text = self.all_songs[0]
				else:
					self.song.text = self.all_songs[self.all_songs.index(self.song.text)+1]

		self.initSong(self.song.text)
		if self.play.source.split('/')[1] != "play.png":
			self.play.source = self.play.source.split('/')[0]+"/play.png"
			self.on_play()


	def previous_song(self):
		self.play.started = 0
		if int(self.ids.duration.text.split('/')[0].split('.')[-1]) < 5:
			# If the song started more than 5 seconds ago it restart the song
			# from the beginning when the previous song button is pressed
			if (self.pressed_back):
				self.pressed_back += 1
				self.song.text = self.last_songs[-self.pressed_back]
			else:
				self.song.text = random.choice(self.all_songs)

		self.initSong(self.song.text)
		if self.play.source.split('/')[1] != "play.png":
			self.play.source = self.play.source.split('/')[0]+"/play.png"
			self.on_play()


	def on_play(self):
		if self.play.source.split('/')[1] == "play.png":
			if self.play.started:
				music.unpause()
			else:
				music.load(music_path+self.song.text)
				music.play()
				self.play.started = 1
			self.play.source = self.play.source.split('/')[0]+"/stop.png"
			Clock.schedule_interval(self.update, 0.1)
		else:
			music.pause()
			self.play.source = self.play.source.split('/')[0]+"/play.png"
			Clock.unschedule(self.update)


	def on_shuffle(self):
		if self.ids.shuffle.source.split('/')[1] == "shuffle.png":
			self.ids.shuffle.source = self.ids.shuffle.source.split('/')[0] + '/shuffle_pressed.png'
			self.randomSongs = True
		else:
			self.ids.shuffle.source = self.ids.shuffle.source.split('/')[0] + '/shuffle.png'
			self.randomSongs = False

	def check_volume(self, *args):
		music.set_volume(args[1])

		if self.ids.volumeImage.source.split('/')[1] == 'volume.png':
			if not self.ids.volume.value:
				self.ids.volumeImage.source = self.ids.volumeImage.source.split('/')[0]+'/mute.png'
		else:
			if self.ids.volume.value:
				self.ids.volumeImage.source = self.ids.volumeImage.source.split('/')[0]+'/volume.png'

class MusicApp(App):

	def build(self):
		Window.size = (400, 100)
		Window.title = "Music Player"
		return MainScreen()


if __name__ == '__main__':
    MusicApp().run()
