class MyError(Exception):
	def __init__(self, err_msg):
		self.err_msg = err_msg
	def __str__(self):
		return repr(self.err_msg)