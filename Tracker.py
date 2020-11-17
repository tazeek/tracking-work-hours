from datetime import datetime, timedelta, time

class Tracker:

	def __init__(self):

		self._total_minutes_hour = 60
		self._daily_hours_cover = 8
		self._num_working_days = 5

		self._total_target_hours = self._num_working_days * self._daily_hours_cover
		self._max_minutes_daily = self._daily_hours_cover * self._total_minutes_hour
		self._max_minutes_weekly = self._num_working_days * self._max_minutes_daily
		self._overtime_hours = self._total_minutes_hour * (self._daily_hours_cover + 1)

		self._before_noon_minutes_covered = 0
		self._after_noon_minutes_covered = 0
		self._remaining_today = 0
		self._remaining_week = 0

		self._days_information_array = []

		self._day_number = self._get_day_number()
		self._file_name = 'folder/working_hours.txt'

	def get_max_minutes_daily(self):
		return self._max_minutes_daily

	def get_total_time_covered(self):
		return self._before_noon_minutes_covered + self._after_noon_minutes_covered

	def get_remaining_weekly(self):
		return self._remaining_week

	def get_days_stats(self):
		return self._days_information_array

	def get_after_noon_minutes(self):
		return self._after_noon_minutes_covered

	def get_before_noon_minutes(self):
		return self._before_noon_minutes_covered

	def get_hours_minutes(self,total_minutes):
		hours, minutes = divmod(total_minutes, self._total_minutes_hour)

		return str(hours) + 'h ' + str(minutes) + 'm'

	def _get_current_time(self):
		return str(datetime.now().hour) + ':' + str(datetime.now().minute)

	def _get_day_number(self):
		return datetime.today().weekday()

	def _convert_duration_to_minutes(self,start_time, end_time):

		FMT = '%H:%M'

		diff = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)

		return diff.seconds/60

	def _analyze_times_different_period(self, start_time, end_time):

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

		total_minutes_before_noon = 0
		total_minutes_after_noon = 0

		for hours in times:

			hours = hours.rstrip('\n')

			# Each time gap has two outcomes: 
			# 1. 1400-1800 (240 minutes)
			 # 2. 0800- (Current time)
			(start_time, end_time) = hours.split('-')
			end_time = end_time if end_time != '' else self._get_current_time()

			before_noon_minutes, after_noon_minutes = self._analyze_times_different_period(start_time, end_time)

			total_minutes_before_noon += before_noon_minutes
			total_minutes_after_noon += after_noon_minutes

		return total_minutes_before_noon, total_minutes_after_noon

	def _find_time_covered_today(self,remaining_today):

		covered_today = 0

		if remaining_today > 0:

			covered_today = self._max_minutes_daily - remaining_today
			self._finishing_time_today = datetime.now() + timedelta(minutes = remaining_today)

		else:

			covered_today = self._max_minutes_daily

		return covered_today

	def find_average_time_to_cover(self):

		today_stats = self._days_information_array[self._day_number]

		total_time_exclude_today = self._max_minutes_weekly - (self.get_total_time_covered() - today_stats['minutes_covered'])
		days_remaining = self._num_working_days - self._day_number

		# Find the average and increment it with the remainder as well
		# REASON: Better to cover more minutes than not to
		avg_mins, remainder = divmod(total_time_exclude_today, (days_remaining))
		total_avg = avg_mins + remainder

		avg_hour, avg_mins = divmod(total_avg, self._total_minutes_hour)

		avg_time_str_format = str(avg_hour) + 'h ' + str(avg_mins) + 'm'

		return total_avg, avg_time_str_format

	def update_time_calculations(self):

		remaining_today = 0
		remaining_weekly = 0

		# One line = Day, Time gap #1, Time gap #2, ..., Time gap n
		with open(self._file_name) as file:

			for index, line in enumerate(file):

				line_array = line.replace('\x00','').rstrip().split(',')

				day = line_array[0]
				day_coverage_array = line_array[1:]

				total_minutes_before_noon, total_minutes_after_noon = self._perform_noon_time_comparisons(day_coverage_array)

				self._before_noon_minutes_covered += total_minutes_before_noon
				self._after_noon_minutes_covered += total_minutes_after_noon

				total_minutes_day = total_minutes_before_noon + total_minutes_after_noon

				self._days_information_array.append({
					'day': day,
					'minutes_covered': total_minutes_day,
					'coverage': day_coverage_array
				})

				if index == self._day_number:

					self._remaining_today = self._max_minutes_daily - total_minutes_day

			total_covered = self.get_total_time_covered()

			if total_covered < self._max_minutes_weekly:
				self._remaining_week = self._max_minutes_weekly - total_covered

		return None
