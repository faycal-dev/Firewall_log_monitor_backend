import json
from channels.generic.websocket import WebsocketConsumer
import threading
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle

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
    sc = pickle.load(
        open('C:/Users/hp/Desktop/PFE/Back/app/ai/scaler.pkl', 'rb'))
    model = load_model(
        'C:/Users/hp/Desktop/PFE/Back/app/ai/anomaly_detector.h5')
    model.load_weights(
        'C:/Users/hp/Desktop/PFE/Back/app/ai/anomaly_detector.weights.h5')

    def preprocess(self, df):
        df = df[['proto', 'state', 'dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'sttl',
                 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit',
                 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat',
                 'smean', 'dmean', 'ct_srv_src', 'ct_dst_ltm', 'ct_src_dport_ltm',
                 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_src_ltm', 'ct_srv_dst',
                 'is_sm_ips_ports']]

        hot_coded_1 = ['None', 'arp', 'ospf', 'tcp', 'udp', 'unas']
        hot_coded_2 = ['CON', 'FIN', 'INT', 'None', 'REQ', 'RST']
        X = []
        for i in hot_coded_1:
            if (df['proto'] == i):
                X.append(1)
            else:
                X.append(0)
        for i in hot_coded_2:
            if (df['state'] == i):
                X.append(1)
            else:
                X.append(0)
        df.drop(["proto", "state"], inplace=True)
        df = df.to_list()
        X = np.concatenate((X, df), axis=0)
        # now we will standerize the data the first 12 column is categorical we won't std them
        X = np.array(X)
        X = np.expand_dims(X, axis=0)
        X[:, 13:] = self.sc.transform(X[:, 13:])
        X = X.reshape(1, 1, 44)
        prediction = self.model.predict(X)
        if (np.argmax(prediction[0][0]) == 1 and prediction[0][0][1] > 0.97):
            return 1
        return 0

    def send_logs(self):
        logs = self.search_document.search().sort(
            {"@timestamp": {"order": "desc"}})[0:100].execute()
        serializedResult = self.logs_serializer(logs, many=True)
        pd_response = pd.DataFrame(serializedResult.data)
        for i in range(pd_response.shape[0]):
            if (pd_response.iloc[i]["Action"] in ['built', 'accept', 'successful']):
                if (self.preprocess(pd_response.iloc[i]) == 1):
                    json_anomaly = {"Anomaly": True,
                                    "data": pd_response.iloc[i].to_dict()}
                    self.send(json.dumps(json_anomaly))
                    break
        self.send(json.dumps(serializedResult.data))

    def connect(self):

        self.accept()
        logs = self.search_document.search().sort(
            {"@timestamp": {"order": "desc"}})[0:100].execute()
        serializedResult = self.logs_serializer(logs, many=True)
        pd_response = pd.DataFrame(serializedResult.data)
        for i in range(pd_response.shape[0]):
            if (pd_response.iloc[i]["Action"] in ['built', 'accept', 'successful']):
                if (self.preprocess(pd_response.iloc[i]) == 1):
                    json_anomaly = {"Anomaly": True,
                                    "data": pd_response.iloc[i].to_dict()}
                    self.send(json.dumps(json_anomaly))
                    break
        self.send(json.dumps(serializedResult.data))
        event = threading.Event()
        k = ThreadJob(self.send_logs, event, 2)
        k.start()
        self.kThread = k

    def disconnect(self, code):
        self.kThread.join()
