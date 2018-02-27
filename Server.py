from random import random
import numpy as np


class Server:

	def __init__(self, fun):
		self.fun = fun

	def get_list(self, n):
		arr = []
		for _ in range(n):
			arr.append(random())
		return self.fun(np.array(arr))
