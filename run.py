#!/usr/bin/env python3

import pynput
import time
import sys
import os
import csv
import action
from enum import Enum

recordMouseMov = False

actions = []

XPOS = 0
YPOS = 1
BUTTON = 2
PRESS = 3
CLICKLEN = 4

KEY = 0
KEYSTATE = 1
KEYLEN = 2

XPOS = 0
YPOS = 1
DX = 2
DY = 3
SCROLLLEN = 4

def main():
	fileName = ""

	record = True

	if len(sys.argv) > 1:
		fileName = sys.argv[1] 

	if fileName == "":
		print("please specify a filename")
		return 1

	fileName = os.path.join("actionFiles", fileName)

	if not os.path.isfile(fileName):
		print("there's no file by the name of {0}".format(fileName))
		return 2


	file = open(fileName, "r")
	getActionsFromFile(file)
	for act in actions:
		act.doAction()
	file.close()

def getActionsFromFile(file):
	reader = csv.reader(file)
	data = list(reader)
	for d in data:
		if d[0] == "click":
			actions.append(clickParse(d))
		elif d[0] == "key":
			actions.append(keyParse(d))

def clickParse(data):
	button = None

	if data[BUTTON + 1] == "Button.left":
		button = pynput.mouse.Button.left
	elif data[BUTTON + 1] == "Button.middle":
		button = pynput.mouse.Button.middle
	elif data[BUTTON + 1] == "Button.right":
		button = pynput.mouse.Button.right

	return action.action(data[0], 
		(int(data[XPOS+1]), int(data[YPOS+1]), button, data[PRESS+1] == "True"), 
		float(data[CLICKLEN + 1]))

def keyParse(data):
	key = None

	if data[KEY + 1] == "Key.up":
		key = pynput.keyboard.Key.up
	elif data[KEY + 1] == "Key.right":
		key = pynput.keyboard.Key.right
	elif data[KEY + 1] == "Key.down":
		key = pynput.keyboard.Key.down
	elif data[KEY + 1] == "Key.left":
		key = pynput.keyboard.Key.left
	elif data[KEY + 1] == "Key.backspace":
		key = pynput.keyboard.Key.backspace
	elif data[KEY + 1] == "Key.ctrl":
		key = pynput.keyboard.Key.ctrl
	elif data[KEY + 1] == "Key.shift":
		key = pynput.keyboard.Key.shift
	elif data[KEY + 1] == "Key.alt":
		key = pynput.keyboard.Key.alt
	elif data[KEY + 1] == "Key.tab":
		key = pynput.keyboard.Key.tab
	elif data[KEY + 1] == "Key.enter":
		key = pynput.keyboard.Key.enter
	else:
		key = data[KEY+1][1]

	return action.action(data[0],
		(key, data[KEYSTATE+1] == "True"),
		float(data[KEYLEN+1]))

if __name__ == "__main__":
	main()