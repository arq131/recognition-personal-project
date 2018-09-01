import kivy.core.text
import cv2
import os

from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.button import Button

image_count = 0
record_status = False
inputs = ''
class KivyCamera(Image):
	def __init__(self, **kwargs):
		super(KivyCamera, self).__init__(**kwargs)
		self.capture = None

	def start(self, capture, fps=30):
		self.capture = capture
		Clock.schedule_interval(self.update, 1.0 / fps)

	def stop(self):
		Clock.unschedule(self.update)
		self.canvas.clear()
		self.capture = None

	def update(self, dt):
		global record_status
		global image_count
		global inputs
		ret, frame = self.capture.read()

		texture = self.texture
		# Example for screen capture. 
		# Use this to save face image to a file
		#cv2.COLOR_BGR2GRAY
		if record_status and (inputs != ''):
			# Convert image to greyscale
			img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			
			inputs = inputs.replace(' ', '_')

			# If there's no existing directory for the user's name
			if not os.path.isdir('test-data/' + str(inputs)):
				os.mkdir('test-data/' + str(inputs))
			cv2.imwrite('test-data/' + str(inputs) + '/' + str(image_count) + '.png', img)
			image_count = image_count + 1
		
		# Currently ignore video recording
		if ret:
			texture = self.texture
			w, h = frame.shape[1], frame.shape[0] # Width and height of frame
			if not texture or texture.width != w or texture.height != h:
				self.texture = texture = Texture.create(size=(w, h))
				texture.flip_vertical()
			texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
			self.canvas.ask_update()
		

capture = None

class Camera(BoxLayout):
	def init(self):
		pass

	def dostart(self, *args):
		global capture
		global inputs
		capture = cv2.VideoCapture(0)
		

		# Change the settings on the button
		if not self.ids.start.status:
			self.ids.start.text = 'Stop Camera'
			self.ids.start.color = [1, 0, 0, 1]
			self.ids.start.status = True
			self.ids.cam.start(capture)
		else:
			self.ids.start.text = 'Start Camera'
			self.ids.start.color = [0, 1, 0, 1]
			self.ids.start.status = False
			self.ids.cam.stop()


		inputs = self.ids.name.text



	def doexit(self):
		global capture
		if capture != None:
			capture.release()
			capture = None
		EventLoop.stop()

	# Start the recording and file-saving
	def dorecord(self):
		global record_status
		if not record_status: # Tint the background of the record button a bit red
			self.ids.record.background_normal = ''
			self.ids.record.background_color = [1, 0, 0, .3]
			record_status = True
		else: # Return to default values
			self.ids.record.background_normal = 'atlas://data/images/defaulttheme/button'
			self.ids.record.background_color = [1, 1, 1, 1]
			record_status = False

	def name_click(self):
		self.ids.name.text = ''



class CameraApp(App):
	kv_directory = 'kvfiles'
	filler_color = [0, 0, 0, 1]

	def build(self):
		Window.clearcolor = (.4,.4,.4,1)
		Window.size = (480, 940)
		homeWin = Camera()
		homeWin.init()
		return homeWin

	def on_stop(self):
		global capture
		if capture:
			capture.release()
			capture = None

if __name__ == "__main__":
	CameraApp().run()