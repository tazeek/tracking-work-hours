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

	def