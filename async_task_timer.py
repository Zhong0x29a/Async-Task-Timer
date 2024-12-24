import contextvars
import threading
from typing import Tuple

from data_structure import ThreadSafeDict


class AsyncTaskTimer:

	def __init__(self):
		self.__timer_task_map = ThreadSafeDict()

	def add_or_update_task(self, exe_time: float | int, func: callable, *args, notify_func: callable = None,
	                       notify_func_args: Tuple=None,):
		"""
		:*args is a tuple, could not contain list! Otherwise, will raise Unhashable type: 'list'.
		"""
		self.del_timer(func, *args)
		self.set_timer(exe_time, func, *args, notify_func=notify_func, notify_func_args=notify_func_args)

	def set_timer(self, exe_time, func, *args, notify_func=None, notify_func_args=None):
		def target_func(ctx):
			ctx.run(func, *args)
			if notify_func:
				ctx.run(notify_func, *notify_func_args)
		timer = threading.Timer(exe_time, target_func, args=(contextvars.copy_context(), ))
		timer.start()
		self.__timer_task_map[(func, *args)] = [exe_time, timer]

	def del_timer(self, func, *args):
		if (func, *args) in self.__timer_task_map:
			item: list[float, threading.Timer] = self.__timer_task_map.pop((func, *args))
			if item[1].is_alive():
				item[1].cancel()
			else:
				del item


''' Test Code below. '''
if __name__ == '__main__':
	import time
	from time import sleep

	start_time = time.time()
	test_id = contextvars.ContextVar("test_id", default="TEST_ID")


	def test(*args):
		print(f'time: {(time.time() - start_time):.2f}, \t\t test{args}', end='\t')
		print(f'{test_id.get()=}')


	def test2(a, b='null', c='null'):
		print(f'time: {(time.time() - start_time):.2f}, \t\t test2({a=}, {b=}, {c=})', end='\t')
		print(f'{test_id.get()=}')



	def notify_test(msg, test_arg='null'):
		print(f'time: {(time.time() - start_time):.2f}, \t\t notify_test({msg=}, {test_arg=})', end='\t')
		print(f'{test_id.get()=}')


	timer_task = AsyncTaskTimer()
	test_id.set('1')
	timer_task.add_or_update_task(5, test)
	test_id.set('2')
	timer_task.add_or_update_task(6, test2, 'a1', 'b1', 'c1',
	                              notify_func=notify_test, notify_func_args=('test msg','arg2'))
	test_id.set('3')
	timer_task.add_or_update_task(7, test2, 'a1', 'b1')
	test_id.set('4')
	timer_task.add_or_update_task(8, test, 1, 2, 3)
	sleep(1)
	test_id.set('5')
	timer_task.add_or_update_task(2, test)

	timer_task.del_timer(test, 1, 2, 3)

'''Output:
time: 3.01, 		 test()	test_id.get()='5'
time: 6.01, 		 test2(a='a1', b='b1', c='c1')	test_id.get()='2'
time: 6.01, 		 notify_test(msg='test msg', test_arg='arg2')	test_id.get()='2'
time: 7.01, 		 test2(a='a1', b='b1', c='null')	test_id.get()='3'

Process finished with exit code 0
'''
