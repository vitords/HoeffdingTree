import math
import core.utils

class ContingencyTables(object):
	"""docstring for ContingencyTables"""
	def __init__(self):
		pass

	@staticmethod
	def entropy(array):
		return_value = 0
		sum_value = 0

		for i in range(len(array)):
			return_value -= ContingencyTables.ln_func(array[i])
			sum_value += array[i]
		if utils.eq(sum_value, 0):
			return 0
		else:
			return (return_value + ContingencyTables.ln_func(sum_value)) / (sum_value * math.log(2))

	@staticmethod
	def ln_func(num):
		if num <= 0:
			return 0
		else:
			return num * math.log(num)
		