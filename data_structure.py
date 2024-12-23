import threading


class ThreadSafeDict(dict):
	"""
	Thread safe dictionary. This class is used to store data when we are not sure if the data is accessed from multiple threads or not.

	Example:

		# Create a thread safe dict
		threads_dict = ThreadSafeDict()

		# Set a value
		threads_dict.set("key", "value")

		# Get a value
		value = threads_dict.get("key")
	"""
	def __init__(self):
		self.lock = threading.Lock()
		super().__init__()

	def set(self, key, value):
		with self.lock:
			super().setdefault(key, value)

	def get(self, key, default=None):
		with self.lock:
			return super().get(key, default)

	def pop(self, key, default=None):
		with self.lock:
			return super().pop(key, default)

	def __setitem__(self, key, value):
		with self.lock:
			super().__setitem__(key, value)

	def __getitem__(self, key):
		with self.lock:
			return super().__getitem__(key)

	def __delitem__(self, key):
		with self.lock:
			super().__delitem__(key)

	def __contains__(self, key):
		with self.lock:
			return super().__contains__(key)


''' Test Code below. '''
if __name__ == '__main__':
	test_dict = ThreadSafeDict()
