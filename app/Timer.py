from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
import time
import math

class ClockWidget(Widget):
	def __init__(self):
		self.centerX = 400
		self.centerY = 400
		self.len = 50


	def update(self, *args):
		self.text = time.asctime()

	def draw(self, *args):
		print("hello")
		while True:
			self.local = time.localtime(time.time()) # Returns hour, mins, seconds
			self.hours = local[3]
			self.posX = self.len * math.cos(math.radians(hours * 6) - math.radians(90)) + self.centerX # hours 120 ticks
			self.posY = self.len * math.sin(math.radians(hours * 6) - math.radians(90)) + self.centerX
			self.line = Line([self.centerX, self.centerY, self.posX, self.posY], width=2) # [x1, y1, x2, y2] -- [400, 400] center; lets set 12: [400, 200], 3 = [600, 400], 6 = [400, 600], 9 = [200, 400] 


	'''
	Main logic required:
	- Analog picture
	- How to draw the hands
	- Figure out timing of pixel to 
	360 degrees
	360/12 = 30
	30 ticks per hour at most.
	if set to 4 ticks in each, minute hand will move every 15 minutes ?


	Seperate each time into sections:

	Hours: 12 main ticks (every 10 = 1 hour)
	Minutes: 120 main ticks (every 12 = 1 min mins)  
	Seconds
	'''


class TimeApp(App):
	def build(self):
		timer = ClockWidget()
		Clock.schedule_interval(timer.draw, 1)
		return timer

if __name__ == "__main__":
	TimeApp().run()

