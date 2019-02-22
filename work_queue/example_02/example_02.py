import work_queue as WQ

# in case we want ${USER} for master name
from os import environ
import time

#### Customize your master name
master_name = environ['USER'] + '-master'

# run at some port at random
q = WQ.WorkQueue(name=master_name, port=0)

# enable the transactions log
q.specify_transactions_log('my_transactions.log')

print 'WorkQueue on port: {}'.format(q.port)

# enable the measuring of resources
q.enable_monitoring()

# create a category for all tasks
q.specify_category_max_resources('my-tasks', {'cores': 1, 'disk': 500})
q.specify_category_mode('my-tasks', WQ.WORK_QUEUE_ALLOCATION_MODE_MAX_THROUGHPUT)

# create 30 tasks. Each task simply creates a 200MB file, using 10MB of memory
# buffer.
for i in range(0,30):
    t = WQ.Task('python task.py')
    t.specify_input_file('task.py', cache = True)
    t.specify_category('my-tasks')
    t.specify_max_retries(2)
    q.submit(t)

# create a task that will break the limits set
t = WQ.Task('python task.py 1000')
t.specify_input_file('task.py', cache = True)
t.specify_category('my-tasks')
t.specify_max_retries(2)
q.submit(t)


# wait for task to finish
while not q.empty():
    t = q.wait(60)
    if t:
        print 'task {} finished:'.format(t.id)
	print 'allocated mem {} disk {}, used mem {} disk {}'.format(t.resources_allocated.memory,
                                                                     t.resources_allocated.disk,
                                                                     t.resources_measured.memory,
                                                                     t.resources_measured.disk)
print 'Now in a terminal, type:'
print 'work_queue_status -A localhost {}'.format(q.port)

raw_input('\n\nPress enter to exit master')




