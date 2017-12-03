from enum import Enum
import time
import pynput

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

XPOS = 0
YPOS = 1
BUTTON = 2
PRESS = 3

KEY = 0
KEYSTATE = 1

XPOS = 0
YPOS = 1
DX = 2
DY = 3

class action:
	def __init__(self, action, data, delay = 0.2):
		self.type = action
		self.data = data
		self.delay = delay

	def doAction(self):
		time.sleep(self.delay)
		if self.type == "click":
			self._click()
		elif self.type == "key":
			self._pressKey()
		elif self.type == "move":
			self._move()
		elif self.type == "scroll":
			self._scroll()

	def _click(self):
		mouse.position = self.data[XPOS], self.data[YPOS]
		if self.data[PRESS]:
			mouse.press(self.data[BUTTON])
		else:
			mouse.release(self.data[BUTTON])

	def _pressKey(self):
		if self.data[KEYSTATE]:
			keyboard.press(self.data[KEY])
		else:
			keyboard.release(self.data[KEY])

	def _move(self):
		return 0

	def _scroll(self):
		mouse.position = self.data[XPOS], self.data[YPOS]
		mouse.scroll(self.data[2], self.data[3])

