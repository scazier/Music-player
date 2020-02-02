import pyaudio
import wave
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader


Config.set('graphics','resizable', False)

class ImageButton(ButtonBehavior, Image):
	pass

class MainScreen(Widget):
	pass

class MusicApp(App):

	def build(self):
		Window.size = (400, 100)
		return MainScreen()


if __name__ == '__main__':
    MusicApp().run()
