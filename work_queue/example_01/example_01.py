import work_queue as WQ

# in case we want ${USER} for master name
from os import environ

#### SET MASTER NAME HERE
#### for example: master_name = environ['USER'] + '-my-first-master'

master_name = NOT_SET

# 1. run at some port at random
q = WQ.WorkQueue(name=master_name, port=0)

# 2. create a tasks that runs a command remotely, and ...
t = WQ.Task('./sim.exe A B')

# ...specify the name of input and output files
t.specify_input_file('sim.exe', cache=True)
t.specify_input_file('A')
t.specify_output_file('B')

# 3. submit the task to the queue
q.submit(t)

# 4. wait for all tasks to finish, 5 second timeout:
while not q.empty():
    t = q.wait(5)
    if t:
        print 'task {} finished'.format(t.id)

