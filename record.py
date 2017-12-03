#!/usr/bin/env python3
import time
import pynput
import action
import csv
import sys
import os

prevX = 100000
prevY = 100000

xbeforeNew = 20
ybeforeNew = 20

actions = []

lastTime = time.time()

def getDelay():
	global lastTime
	temp = time.time() - lastTime
	lastTime = time.time()
	return float("%.4f"%temp)

def main():

	fileName = ""

	if len(sys.argv) <= 1:
		print("usage: run.py name_of_file")
		return 1
	
	fileName = sys.argv[1]

	fileName = os.path.join("actionFiles", fileName)

	if os.path.isfile(fileName):
		print("that filename already exist, do you want to replace it?")
		inp = input("[Y/N] ")
		if inp == "n" or inp == "N":
			return 2
		elif inp != "y" and inp != "Y":
			return 3

	recordActions()
	file = open(fileName, "w")
	saveActionsInFile(file)
	file.close()

def recordPress(key):
	if (key == pynput.keyboard.Key.esc):
		print("escape")
		return False
	de = getDelay()
	print("{0}".format(("key", (str(key), True, de))))
	actions.append(action.action("key", (str(key), True), de) )

def recordRelease(key):
	actions.append(action.action("key", (str(key), False), getDelay() ) )	

def onMove(x, y):
	return True

def recordClick(x, y, button, pressed):

	if action.mouse.position == (0,0):
		return False

	de = getDelay()

	if pressed:
		print("{0}".format((x, y, button, de)))

	actions.append(action.action("click", (x, y, button, pressed), de))

def onScroll(x, y, dx, dy):
	actions.append(action.action("scroll", (x, y, dx, dy)))

def recordActions():
	with pynput.keyboard.Listener( on_press = recordPress, on_release = recordRelease) as listener:
		with pynput.mouse.Listener(on_move = onMove, on_click = recordClick, on_scroll = onScroll) as m:
			listener.join()
			m.join()

def saveActionsInFile(file):
	writer = csv.writer(file)

	for action in actions:
		writer.writerow([action.type] + list(action.data) + [action.delay] )
		
	return True

if __name__ == "__main__":
	main()
