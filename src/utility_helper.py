import time

def validate_coverage(coverage):

	if not coverage:
		return True

	if len(coverage) != 5:
		return False

	try:
		time.strptime(coverage, '%H:%M')
		return True
	except ValueError:
		return False

	return False