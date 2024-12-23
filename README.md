# Async-Task-Timer

## Example: 
```python
import time
from time import sleep

start_time = time.time()


def test(*args):
    print(f'time: {int(time.time() - start_time)}, \t\t test{args}')


def test2(a, b='null', c='null'):
    print(f'time: {int(time.time() - start_time)}, \t\t test2({a=}, {b=}, {c=})')


def notify_test(msg):
    print(f'time: {int(time.time() - start_time)}, \t\t notify_test({msg=})')


timer_task = AsyncTaskTimer()
timer_task.add_or_update_task(5, test)
timer_task.add_or_update_task(6, test2, 'a1', 'b1', 'c1',
                                notify_func=notify_test, notify_func_args=('test msg',))
timer_task.add_or_update_task(7, test2, 'a1', 'b1')
timer_task.add_or_update_task(8, test, 1, 2, 3)
sleep(1)
timer_task.add_or_update_task(2, test)

timer_task.del_timer(test, 1, 2, 3)
```

```Output:
time: 3, 		 test()
time: 6, 		 test2(a='a1', b='b1', c='c1')
time: 6, 		 notify_test(msg='test msg')
time: 7, 		 test2(a='a1', b='b1', c='null')

Process finished with exit code 0
```