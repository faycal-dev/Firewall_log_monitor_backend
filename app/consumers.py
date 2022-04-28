import json
from channels.generic.websocket import WebsocketConsumer
import threading

from app.serializers import LogsSerializer
from .documents import LogsDocument


class ThreadJob(threading.Thread):
    def __init__(self, callback, event, interval):
        '''runs the callback function after interval seconds

        :param callback:  callback function to invoke
        :param event: external event for controlling the update operation
        :param interval: time in seconds after which are required to fire the callback
        :type callback: function
        :type interval: int
        '''
        self.callback = callback
        self.event = event
        self.interval = interval
        super(ThreadJob, self).__init__()

    def run(self):
        while not (self.event.wait(self.interval) & self.event.isSet()):
            self.callback()
    
    def join(self, timeout=None):
        """ Stop the thread. """
        self.event.set()
        threading.Thread.join(self, timeout)

class LogsConsumer(WebsocketConsumer):
    logs_serializer = LogsSerializer
    search_document = LogsDocument
    kThread = None
    
    def send_logs(self):
        logs = self.search_document.search().sort({"@timestamp" : {"order" : "desc"}})[0:100].execute()
        serializedResult = self.logs_serializer(logs, many=True)
        self.send(json.dumps(serializedResult.data))

    def connect(self):

        self.accept()
        logs = self.search_document.search().sort({"@timestamp" : {"order" : "desc"}})[0:100].execute()
        serializedResult = self.logs_serializer(logs, many=True)        
        self.send(json.dumps(serializedResult.data))
        event = threading.Event()
        k = ThreadJob(self.send_logs, event, 2)
        k.start()
        self.kThread = k


    def disconnect(self, code):
        self.kThread.join()


