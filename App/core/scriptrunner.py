import multiprocessing
import time

class Worker(multiprocessing.Process):
    def __init__(self, task_queue, message_queue):
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.message_queue = message_queue

    def run(self):
        task = self.task_queue.get()

        while task:
            print('Starting:', task.name)
            task.execute(self.message_queue)
            print('Finished:', task.name)
            task = self.task_queue.get()

class ParallelScriptRunner(object):
    def __init__(self, scripts, simultaneous_processes):
        self.task_queue = multiprocessing.Queue()
        self.message_queue = multiprocessing.Queue()
        self.processes = [Worker(self.task_queue, self.message_queue) for i in range(simultaneous_processes)]

        for script in scripts:
            self.task_queue.put(script)

        for process in self.processes:
            self.task_queue.put(None) # Sentinel indicating queue is empty, one per process because it is removed from queue when read

    def run(self):
        for process in self.processes:
            process.start()

        while self.is_running():
            time.sleep(0.5)

    def is_running(self):
        for process in self.processes:
            if process.is_alive():
                return True

        return False

    def terminate(self):
        for process in self.processes:
            process.terminate()

    def receive_messages(self):
        changed = False

        while True:
            try:
                message = self.message_queue.get(block=False) # A message is just a task object
            except queue.Empty:
                break

            changed = True
            setattr(self.task_map[message.task_name], message.type, message.value)

        if changed:
            pub.publish('tasks_changed', self.get_tasks())
