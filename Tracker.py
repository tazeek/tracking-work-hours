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

		self._before_noon_minutes = 0
		self._after_noon_minutes = 0

	def _get_current_time(self):
		return str(datetime.now().hour) + ':' + str(datetime.now().minute)

	def _get_day_number(self):
		return datetime.today().weekday()

	def _get_hours_minutes(self,total_minutes):
		hours, minutes = divmod(total_minutes, self._total_minutes_hour)

		return hours, minutes

	def _convert_duration_to_minutes(self,start_time, end_time):

		FMT = '%H:%M'

		diff = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)

		return diff.seconds/60

	def _analyze_times_different_period(self, start_time, end_time):

		start_time_hour = int(start_time.split(':')[0])
		end_time_hour = int(end_time.split(':')[0])
		mid_day_time = time(12,00)

		time_in_same_period = convert_duration_to_minutes(start_time,end_time)

		# If the end duration is not after noon, then
		# the first duration is for sure not after noon
		if time(end_time_hour,00) >= mid_day_time:

			if time(start_time_hour,00) >= mid_day_time:
				after_noon_minutes = time_in_same_period
			else:
				before_noon_minutes += convert_duration_to_minutes(start_time,'12:00')
				after_noon_minutes += convert_duration_to_minutes('12:00',end_time)
		else:
			before_noon_minutes = time_in_same_period

		return before_noon_minutes, after_noon_minutes

	def _perform_daily_time_analysis(self,times):

		for hours in times:

			hours = hours.rstrip('\n')

			# Each time gap has two outcomes: 
			# 1. 1400-1800 (240 minutes)
			 # 2. 0800- (Current time)
			(start_time, end_time) = hours.split('-')
			end_time = end_time if end_time != '' else self._get_current_time()

			before_noon_minutes, after_noon_minutes = self._analyze_times_different_period(start_time, end_time)
			self._before_noon_minutes += before_noon_minutes
			self._after_noon_minutes += after_noon_minutes

		return None