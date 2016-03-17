import math

def normalize(floats, floats_sum=None):
	if floats_sum is None:
		floats_sum = 0.0
		for i in range(len(floats)):
			floats_sum += floats[i]
		normalize(floats, floats_sum)
	if math.isnan(floats_sum):
		raise ValueError("Can't normalize list. Sum is NaN.")
	if floats_sum is 0:
		raise ValueError("Can't normalize list. Sum is zero.")
	for i in range(len(floats_sum)):
		floats_sum /= floats_sum

def sort(split_candidates):
	pass

def compare(f1, f2):
	"""Compare two float values.
	"""
	if f1 < f2:
		return -1
	if f1 > f2:
		return 1
	# Values are equal
	return 0

def normal_probability():
	pass

def is_missing_value(attribute_value):
	pass

def log2(a):
	return math.log(a) / math.log(2)

def eq(a, b):
	# Small deviation allowed in comparisons
	allowed_deviation = 1e-6
	return a is b or ((a - b < allowed_deviation) and (b - a < allowed_deviation))

def entropy(array):
	return_value = 0
	sum_value = 0

	for i in range(len(array)):
		return_value -= ln_func(array[i])
		sum_value += array[i]
	if eq(sum_value, 0):
		return 0
	else:
		return (return_value + ln_func(sum_value)) / (sum_value * math.log(2))

def ln_func(num):
	if num <= 0:
		return 0
	else:
		return num * math.log(num)