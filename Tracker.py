from datetime import datetime, timedelta, time

class Tracker:

	def __init__(self):

		self._total_minutes_hour = 60
		self._daily_hours_cover = 8
		self._num_working_days = 5

		self._max_minutes_daily = self._daily_hours_cover * self._total_minutes_hour
		self._max_minutes_weekly = self._num_working_days * self._max_minutes_daily

		self._remaining_today = 0

		self._days_information_array = []

		self._day_number = self._get_day_number()
		self._file_name = 'folder/working_hours.txt'

		self._update_time_calculations()

	def get_max_minutes_daily(self):
		return self._max_minutes_daily

	def get_days_stats(self):
		return self._days_information_array

	def get_today_coverage(self):
		return ','.join(self._days_information_array[self._day_number]['coverage'])

	def get_hours_minutes(self,total_minutes):
		hours, minutes = divmod(total_minutes, self._total_minutes_hour)

		return str(int(hours)) + 'h ' + str(int(minutes)) + 'm'

	def get_total_and_remaining(self):
		"""Find the total time covered and the total time remaining"""

		total_covered = 0

		for days in self._days_information_array:
			total_covered += days['minutes_before_noon'] + days['minutes_after_noon']

		total_remaining = self._max_minutes_weekly - total_covered
		total_remaining = 0 if total_remaining < 0 else total_remaining

		return total_covered, total_remaining

	def get_current_time(self):

		current_time = datetime.now()

		hour = ''
		minute = ''

		if current_time.hour < 10:
			hour = '0'

		hour += str(current_time.hour)

		if current_time.minute < 10:
			minute = '0'

		minute += str(current_time.minute)

		return hour + ':' + minute

	def get_finishing_time_today(self):
		"""Get the time to finish 8 hours for today"""

		remaining_today = self._remaining_today

		finishing_time_today = '8 hours has been finished. Leave!!'

		if remaining_today > 0:

			finishing_time_today = datetime.now() + timedelta(minutes = remaining_today)
			finishing_time_today = finishing_time_today.time().strftime("%H:%M")

		return finishing_time_today

	def reset_weekly_hours(self):
		"""Remove the coverage of the current week"""

		file = open(self._file_name, 'r+')
		daily_hours = file.readlines()

		days = [day.rstrip().split(',')[0] + '\n' for day in daily_hours]

		file.seek(0)
		file.writelines(days)
		file.truncate()
		file.close()

		return None

	def update_today_coverage(self):

		current_coverage = self._days_information_array[self._day_number]['coverage'][-1]
		current_time = self.get_current_time()

		if current_coverage != '-':
			self._days_information_array[self._day_number]['coverage'].append(current_time)
		else:
			current_coverage += current_time
			self._days_information_array[self._day_number]['coverage'][-1] = current_coverage

		print(self._days_information_array)

		return None

	def _get_day_number(self):
		day_number = datetime.today().weekday()

		# Only weekdays should be counted
		# The last weekday number is 4 (Friday)
		day_number = day_number if day_number < 4 else 4

		return day_number

	def _convert_duration_to_minutes(self,start_time, end_time):
		"""Convert duration between two timeframes into minutes

		Parameters
		----------
			str
				String indicating the start time of coverage
			str
				String indicating the end time of coverage

		Returns
		-----------
			int
				Minutes between two timeframes

		"""

		FMT = '%H:%M'

		diff = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)

		return diff.seconds/60

	def _analyze_times_different_period(self, start_time, end_time):
		"""Find the amount of time covered (before and after noon) between two times

		Parameters
		----------
			str
				String indicating the start time of coverage
			str
				String indicating the end time of coverage

		Returns
		----------
			int
				Amount of time before noon
			int
				Amount of time after noon

		"""

		start_time_hour = int(start_time.split(':')[0])
		end_time_hour = int(end_time.split(':')[0])
		mid_day_time = time(12,00)

		before_noon_minutes = 0
		after_noon_minutes = 0

		time_in_same_period = self._convert_duration_to_minutes(start_time,end_time)

		# If the end duration is not after noon, then
		# the first duration is for sure not after noon
		if time(end_time_hour,00) >= mid_day_time:

			if time(start_time_hour,00) >= mid_day_time:
				after_noon_minutes = time_in_same_period
			else:
				before_noon_minutes += self._convert_duration_to_minutes(start_time,'12:00')
				after_noon_minutes += self._convert_duration_to_minutes('12:00',end_time)
		else:
			before_noon_minutes = time_in_same_period

		return before_noon_minutes, after_noon_minutes

	def _perform_noon_time_comparisons(self,times):
		"""Find the total amount of time covered before and after noon
		
		Parameter
		---------
			str
				Coverage of the day (ex. '8:00-11:39,11:45-12:45')

		Return
		---------

			int
				Total number of minutes covered before noon
			int
				Total number of minutes covered after noon
		"""

		total_minutes_before_noon = 0
		total_minutes_after_noon = 0

		for hours in times:

			hours = hours.rstrip('\n')

			# Each time gap has two outcomes: 
			# 1. 1400-1800 (240 minutes)
			 # 2. 0800- (Current time)
			(start_time, end_time) = hours.split('-')
			end_time = end_time if end_time != '' else self.get_current_time()

			before_noon_minutes, after_noon_minutes = self._analyze_times_different_period(start_time, end_time)

			total_minutes_before_noon += before_noon_minutes
			total_minutes_after_noon += after_noon_minutes

		return total_minutes_before_noon, total_minutes_after_noon

	def perform_live_update(self):
		"""Perform live updates for chart"""

		today_dict = self._days_information_array[self._day_number]
		total_minutes_before_noon, total_minutes_after_noon = self._perform_noon_time_comparisons(today_dict['coverage'])

		self._remaining_today = self._max_minutes_daily - (total_minutes_before_noon + total_minutes_after_noon)

		today_dict['minutes_before_noon'] = total_minutes_before_noon
		today_dict['minutes_after_noon'] = total_minutes_after_noon

		self._days_information_array[self._day_number] = today_dict

		return None

	def _update_time_calculations(self):
		"""Calculate the total time covered and coverage, day by day """

		# One line = Day, Time gap #1, Time gap #2, ..., Time gap n
		with open(self._file_name) as file:

			for index, line in enumerate(file):

				line_array = line.replace('\x00','').rstrip().split(',')

				day = line_array[0]
				day_coverage_array = line_array[1:]

				total_minutes_before_noon, total_minutes_after_noon = self._perform_noon_time_comparisons(day_coverage_array)
				day_total = total_minutes_before_noon + total_minutes_after_noon

				self._days_information_array.append({
					'day': day,
					'minutes_before_noon': total_minutes_before_noon,
					'minutes_after_noon': total_minutes_after_noon,
					'coverage': day_coverage_array
				})

				if index == self._day_number:

					self._remaining_today = self._max_minutes_daily - day_total

		return None
