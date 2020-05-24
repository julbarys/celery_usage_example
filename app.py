import time
import redis
from tasks import *

# call in API
def tasks():
	_redis = redis.Redis(host = '127.0.0.1', port = 6379, decode_responses = True)
	tasks = []
	if _redis.exists('tasks'):
		tasks = json.loads(_redis.get('tasks'))
	return tasks

# call in API
def progress_for_task(task):
	_redis = redis.Redis(host = '127.0.0.1', port = 6379, decode_responses = True)
	progress = 0
	if _redis.exists(f'task:{task}:progress'):
		progress = json.loads(_redis.get(f'task:{task}:progress'))
	return progress

def main():
	# task calling
	_task = long_task.delay(10, 3)

	# progress monitoring
	for i in range(10):
		print(progress_for_task(_task))
		time.sleep(2)


if __name__ == '__main__':
	main()