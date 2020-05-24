import time
import json
import redis
from celery import Celery

app = Celery(
	'tasks',
	broker='redis://localhost',
	backend='redis://localhost'
)

def register_new_task(task):
	_redis = redis.Redis(host = '127.0.0.1', port = 6379, decode_responses = True)
	tasks = []
	if _redis.exists('tasks'):
		tasks = json.loads(_redis.get('tasks'))
	if not task in tasks:
		tasks.append(task)
	_redis.set('tasks', json.dumps(tasks))

@app.task(bind=True)
def long_task(self, count, delay):
	_redis = redis.Redis(host = '127.0.0.1', port = 6379, decode_responses = True)

	# register current task in redis for monitoring
	task_id = self.request.id
	register_new_task(task_id)

	for i in range(count):
		time.sleep(delay)

		# increase progress
		previous_progress = 0
		if _redis.exists(f'task:{task_id}:progress'):
			previous_progress = json.loads(_redis.get(f'task:{task_id}:progress'))
		current_progress = previous_progress + 1
		_redis.set(f'task:{task_id}:progress', json.dumps(current_progress))

	return count * delay
