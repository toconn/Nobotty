#!/usr/bin/env python3

from queue import Queue

from quantumrandom import get_data

QUEUE_SIZE = 50
QUEUE_LOW_SIZE = 10

class Random:

	def __init__(self):
		self._queue = Queue()
		self._refill()

	def boolean(self):
		return self._get_next() > 0.5


	def boolean_weighted(self, weighted):
		''' Returns true in the proportion of the weighted value (.3 = 30% chance)
		'''
		return self._get_next() > (1 - weighted)


	def int (self, value_1, value_2 = None):

		if value_2 == None:
			return self._get_next_int (0, value_1)

		return self._get_next_int (value_1, value_2)


	def pick_one (self, list_1):
		max = len (list_1) - 1
		next = self.int (max)
		print (len(list_1), ":", 0, "..", max, " = ", next)
		return list_1[next]
		# return list_1[self.int (len (list_1) - 1)]


	def _get_next(self):
		next = self._queue.get()
		self._refill()
		return next


	def _get_next_int(self, min, max):
		return int (min + (self._get_next() * (max + 0.999999999 - min)))


	def _is_low(self):
		return self._queue.qsize() < QUEUE_LOW_SIZE


	def _refill(self):

		while self._is_low():
			for data in get_data (array_length = self._refill_count()):
				self._queue.put (data / 65535)

	def _refill_count(self):
		return QUEUE_SIZE - self._queue.qsize()


