
from six.moves.queue import Queue

class Scheduler(object):

    def __init__(self):

        self.queue = Queue()
        self.total_response_nums = 0

    def add_request(self, request):

        self.queue.put(request)
        self.total_response_nums += 1

    def get_request(self):

        return self.queue.get()

    def filter_request(self):
        pass