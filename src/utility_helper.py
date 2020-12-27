import time

def validate_coverage(coverage):

	try:
		time.strptime(coverage, '%H:%M')
		return True
	except ValueError:
		return False