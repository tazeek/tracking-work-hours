from datetime import datetime
from matplotlib import cm

import matplotlib.pyplot as plt
import numpy as np

import math
import getopt, sys

FILE = 'working_hours.txt'

def reset_file():

	file = open(FILE,'r+')
	daily_hours = file.readlines()

	days = [day.rstrip().split(',')[0] + '\n' 
		for day in daily_hours]

	file.truncate(0)
	file.writelines(days)
	file.close()

	return

def update_time():

	day_number = datetime.today().weekday()

	# 1. Open Text file. Get all the times
	# 1 line = 1 day's worth of hours
	file = open(FILE,'r+')

	# 2. Get the current day times
	# Remove the newline string
	daily_hours = file.readlines()
	current_day = daily_hours[day_number].rstrip()

	current_time = str(datetime.now().hour) + ':' + str(datetime.now().minute)

	# 3. Add in the current time to the string (add the extra '-')
	# NOTE: If the last operation was a ',', then there should only be start time
	last_operation = current_day[-1]

	if last_operation == ',':
		current_time += '-'
	elif last_operation != '-':
		current_time = ',' + current_time + '-'

	daily_hours[day_number] = current_day + current_time + '\n'

	# 4. Write the text file
	file.seek(0)
	file.writelines(daily_hours)
	file.close()

	return

def get_arguments_list():

	fullCmdArguments = sys.argv
	argumentList = fullCmdArguments[1:]

	unixOptions = 'usr'
	gnuOptions = ['update', 'reset']

	arguments = None
	values = None

	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:
		print (str(err))
		sys.exit(2)

	return arguments

if __name__== '__main__':

	arguments = get_arguments_list()

	for currentArgument, currentValue in arguments:

		if currentArgument in ('-u', '--update'):
			update_time()

		elif currentArgument in ('-r', '--reset'):
			reset_file()
