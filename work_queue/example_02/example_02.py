import work_queue as WQ

# in case we want ${USER} for master name
from os import environ

#### SET MASTER NAME HERE
#### for example: master_name = environ['USER'] + '-my-first-master'

master_name = NOT_SET

# run at some port at random
q = WQ.WorkQueue(name=master_name, port=0)

print 'WorkQueue on port: {}'.format(q.port)

# enable the measuring of resources
q.enable_monitoring()

# create a category for all tasks
q.specify_category_max_resources('my-tasks', {'cores': 1})

# some resources were specified: memory, and disk will be labeled
# automatically.
q.specify_category_mode('my-tasks', WQ.WORK_QUEUE_ALLOCATION_MODE_MAX_THROUGHPUT)

# create 30 tasks. Each task simply creates a 200MB file, using 10MB of memory
# buffer.
for i in range(0,30):
    t = WQ.Task('python task.py')
    t.specify_input_file('task.py', cache = True)
    t.specify_category('my-tasks')
    t.specify_max_retries(2)
    q.submit(t)

# wait for task to finish
while not q.empty():
    t = q.wait(60)
    if t:
        print 'task {} finished:'.format(t.id)
        if t.result == WQ.WORK_QUEUE_RESULT_SUCCESS:
            print 'allocated mem {} disk {}, used mem {} disk {}'.format(t.resources_allocated.memory,
                                                                         t.resources_allocated.disk,
                                                                         t.resources_measured.memory,
                                                                          t.resources_measured.disk)
        else:
            print 'failed with code {}'.format(t.return_status)

