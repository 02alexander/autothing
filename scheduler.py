#!/usr/bin/env python3

import time
import calendar
import os
from subprocess import call
import sys

startTimeHours = 0
startTimeMinutes = 0

def main():

	fileName = ""

	if len(sys.argv) > 1:
		fileName = sys.argv[1]

	fileName = os.path.join("schedules", fileName)

	if not os.path.isfile(fileName):
		print("there's no file in schedules with that name")
		return 1

	file = open(fileName, "r")

	lines = file.readlines()		

	for d in lines:

		d = parseLine(d)

		t = d[0].split(".")

		hours, minutes = tuple(t)
		hours = int(hours)
		minutes = int(minutes)

		tm = time.gmtime()

		if hours < (tm.tm_hour + 1) % 24 or (hours <= (tm.tm_hour + 1) % 24 and minutes < tm.tm_min):
			continue

		waittil(hours, minutes)

		print(d[2])
		os.system(d[2])

	return 0


def waittil(hours, minutes):
	t = time.gmtime()

	while (hours != (t.tm_hour + 1) % 24 or minutes != t.tm_min): 
		t = time.gmtime()
		time.sleep(1)

# returns a tuple of time to excexute the command, set or relative to x time, command
def parseLine(line):
	tm = ""
	mod = "set" 
	command = ""

	i = 0
	while line[i].isspace():
		i += 1

	if line[i] == '+':
		mod = "rel"
		i += 1

	while line[i].isdigit() or line[i] == '.':
		tm += line[i]
		i += 1
	i += 1

	while line[i].isspace():
		i += 1

	while i < len(line) and line[i] != '\n':
		command += line[i]
		i += 1

	return (tm, mod, command)




if __name__ == "__main__":
	main()