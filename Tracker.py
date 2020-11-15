class Tracker:

	def __init__(self):

		self._total_minutes_hour = 60
		self._daily_hours_cover = 8
		self._num_working_days = 5

		self._total_target_hours = self._num_working_days * self._daily_hours_cover
		self._max_minutes_daily = self._daily_hours_cover * self._total_minutes_hour
		self._max_minutes_weekly = self._num_working_days * self._max_minutes_daily
		self._overtime_hours = self._total_minutes_hour * (self._daily_hours_cover + 1)