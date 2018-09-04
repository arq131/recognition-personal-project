import kivy.core.text
import cv2
import os
import time

from datetime import datetime
from functools import partial

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
haar_path = 'haarcascades/haarcascade_frontalface_default.xml'

class KivyCamera(Image):
	

	def __init__(self, **kwargs):
		super(KivyCamera, self).__init__(**kwargs)
		self.capture = None
		self.start_timer = None
		self.record_timer = False
		self.faceCascade = cv2.CascadeClassifier(haar_path)

	def stop(self):
		Clock.unschedule(self.update)
		self.texture = Texture.create()
		self.capture = None

		
	def start(self, capture, fps=30):
		self.capture = capture
		Clock.schedule_interval(self.update, 1.0 / fps)

	
	def update(self, dt):
		global record_status
		global image_count
		global inputs
		
		ret, frame = self.capture.read()

		texture = self.texture

		# Start recording for 10 seconds, at burst of .5 each (20 total)
		if record_status and inputs != '' and not self.record_timer:
			self.start_timer = time.time()
			image_count = 0
			Clock.schedule_interval(partial(self.save_images, frame), 0.5)
			self.record_timer = True
		
		# If there is a frame that is captured
		if ret:

			# Use Cascading facial recogition to detect the face of the image
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = self.faceCascade.detectMultiScale(
				gray,
				scaleFactor = 1.2,
				minNeighbors = 5,
				minSize = (35, 35),
				flags = cv2.CASCADE_SCALE_IMAGE
				)
			# Draw the rectangle around the face of the frame
			for (x, y, w, h) in faces:
   	 			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

   	 		# Display the frame on the interface
			texture = self.texture
			w, h = frame.shape[1], frame.shape[0] # Width and height of frame
			if not texture or texture.width != w or texture.height != h:
				self.texture = texture = Texture.create(size=(w, h))
				texture.flip_vertical()
			texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
			self.canvas.ask_update()


	'''
		When this method is called, this will start a timer for 10 seconds (or until the record button is stopped)
		and record the image into a folder: test-data/[input-name]/[image-number].png
	'''
	def save_images(self, frame, *args):
		global record_status
		global inputs
		global image_count

		# Make the timer for 10 seconds
		if self.capture == None or (time.time() - self.start_timer > 10):
			self.record_timer = False
			return False
		
		# Convert image to greyscale
		img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		
		inputs = inputs.replace(' ', '_').lower()

		# If there's no existing directory for the test data folder, make it.
		if not os.path.isdir('test-data/'):
			os.mkdir('test-data')

		# If there's no existing directory for the user, make it.
		if not os.path.isdir('test-data/' + str(inputs)):
			os.mkdir('test-data/' + str(inputs))

		cv2.imwrite('test-data/' + str(inputs) + '/' + str(image_count) + '.png', img)
		image_count = image_count + 1

capture = None

class Camera(BoxLayout):
	def init(self):
		pass

	def dostart(self, *args):
		global capture
		global inputs
		
		self.checkName = self.verify_name();
		if not self.checkName:
			print('There are no names being displayed')
			return
		
		inputs = self.ids.name.text
		
		# Change the settings on the button
		if not self.ids.start.status:
			self.ids.start.text = 'Stop Camera'
			self.ids.start.color = [1, 0, 0, 1]
			self.ids.start.status = True

			# Start the camera
			capture = cv2.VideoCapture(0)
			if capture != None:
				self.ids.cam.start(capture)
			else:
				print('There are no cameras attached. Exiting...')
				EventLoop.stop()

		else:
			self.ids.start.text = 'Start Camera'
			self.ids.start.color = [0, 1, 0, 1]
			self.ids.start.status = False

			if capture != None:
				capture.release()
			cv2.destroyAllWindows()

			self.ids.cam.stop()

		



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

	def verify_name(self):
		name = self.ids.name.text
		if (name == None) or (name == ''):
			self.ids.name_label.text = 'Username - Please enter a username.'
			self.ids.name_label.color = [1, 0, 0, 1]
			return False
		return True



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