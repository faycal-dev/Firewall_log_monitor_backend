import json
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Q
from app.documents import LogsDocument
from .serializers import LogsSerializer, MatriceSerializer
from .models import matrice
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle
# from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
# from rest_framework.permissions import AllowAny


class filterLogs(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def get(self, request, query):
        try:
            finalQuery = ' '.join(
                [f'OR ({que})' for que in query.split("&")]).replace("OR", "", 1)
            q = Q("query_string", query=finalQuery, default_field="Severity")
            search = self.search_document.search().query(
                q).sort({"@timestamp": {"order": "desc"}})[0:1000]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializedResult = self.logs_serializer(results, many=True)

            return self.get_paginated_response(serializedResult.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class filterIpLogs(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def get(self, request, query):
        try:
            q = Q("multi_match", query=query, fields=["Destination", "Source"])
            search = self.search_document.search().query(q).sort(
                {"@timestamp": {"order": "desc"}})[0:1000]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializedResult = self.logs_serializer(results, many=True)

            return self.get_paginated_response(serializedResult.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class filterDateLogs(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def get(self, request, query):
        try:
            query = query.split("to")
            q = Q("range", **{'@timestamp': {'gte': int(query[0]),
                                             'lt': int(query[1]), 'format': 'epoch_millis'}})
            search = self.search_document.search().query(q).sort(
                {"@timestamp": {"order": "desc"}})[0:1000]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializedResult = self.logs_serializer(results, many=True)

            return self.get_paginated_response(serializedResult.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class AllLogs(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def get(self, request):
        try:
            search = self.search_document.search().sort(
                {"@timestamp": {"order": "desc"}})[0:1000]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializedResult = self.logs_serializer(results, many=True)

            return self.get_paginated_response(serializedResult.data)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)


class MatriceDeFlux(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def preprocess_source_ip(self, ip):
        try:
            ip = str(ip)
            splited_ip = ip.split(".")
            if (len(splited_ip) != 4):
                return ip
            else:
                cleaned_ip = '.'.join(splited_ip[0:2]) + ".x.x"
                return cleaned_ip
        except:
            return ip

    def get(self, request):

        try:
            GroupBy = request.query_params.get('GroupBy')
            DetailedDest = request.query_params.get('DetailedDest')
            DetailedSrc = request.query_params.get('DetailedSrc')
            search = self.search_document.search().sort(
                {"@timestamp": {"order": "desc"}})
            response = search.execute()
            response = self.logs_serializer(response, many=True)

            # read the response as pandas dataframe
            pd_response = pd.DataFrame(response.data)

            # clean both destination and source ip (10.20.30.40 ==> 10.20.X.X)
            if (DetailedSrc == "yes"):
                pd_response["Source"] = pd_response["Source"].apply(
                    self.preprocess_source_ip)

            if (DetailedDest == "yes"):
                pd_response["Destination"] = pd_response["Destination"].apply(
                    self.preprocess_source_ip)

            # groupe by the cleaned ip to get the matrice
            if (GroupBy == "Source"):
                pd_response = pd_response.groupby(['Source', 'Destination', 'Destination_Service', 'Action'])[
                    "Source"].agg([len]).sort_values(by="len", ascending=False)
            elif (GroupBy == "Destination"):
                pd_response = pd_response.groupby(['Destination', "Source", 'Destination_Service', 'Action'])[
                    "Destination"].agg([len]).sort_values(by="len", ascending=False)
            else:
                pd_response = pd_response.groupby(['Destination_Service', "Source", 'Destination', 'Action'])[
                    "Destination_Service"].agg([len]).sort_values(by="len", ascending=False)

            pd_response.reset_index(inplace=True)
            pd_response = pd_response.to_json(orient="records")

            return JsonResponse(pd_response, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)


class Stats(APIView, LimitOffsetPagination):
    logs_serializer = LogsSerializer
    search_document = LogsDocument

    def preprocess_source_ip(self, ip):
        try:
            ip = str(ip)
            splited_ip = ip.split(".")
            if (len(splited_ip) != 4):
                return ip
            else:
                cleaned_ip = '.'.join(splited_ip[0:2]) + ".x.x"
                return cleaned_ip
        except:
            return ip

    def get(self, request):
        try:

            search = self.search_document.search().sort(
                {"@timestamp": {"order": "desc"}})[0:100000]
            response = search.execute()
            response = self.logs_serializer(response, many=True)

            # read the response as pandas dataframe
            pd_response = pd.DataFrame(response.data)

            Actions = pd_response.Action.value_counts()[:4]
            pd_response["Source"] = pd_response["Source"].apply(
                self.preprocess_source_ip)

            # pd_response["Destination"] = pd_response["Destination"].apply(
            #     self.preprocess_source_ip)

            source_count = pd_response.Source.value_counts()[:7]
            destination_count = pd_response.Destination.value_counts()[:7]

            return JsonResponse({"Actions": Actions.to_json(), "source": source_count.to_json(), "destination": destination_count.to_json()}, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(e, status=500)


class SavedMatrices(APIView):
    serializer_class = MatriceSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)
    
            


class GetSavedMatrices(generics.ListAPIView):
    queryset = matrice.objects.all()
    serializer_class = MatriceSerializer
    
    

class VerifyAnomaly(APIView):
    serializer_class = LogsSerializer
    
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

    def post(self, request):
        try:
            data=request.data,
            pd_response = pd.DataFrame(data[0])
            for i in range(pd_response.shape[0]):
                if (pd_response.iloc[i]["Action"] in ['built', 'accept', 'successful']):
                    if (self.preprocess(pd_response.iloc[i]) == 1):
                        json_anomaly = {"Anomaly": True,
                                        "data": pd_response.iloc[i].to_dict()}
                        print("anomaly")
                        return HttpResponse(json.dumps(json_anomaly), status=status.HTTP_200_OK)
            return HttpResponse(json.dumps({"Anomaly":False}), status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse(json.dumps({"haha":False}), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)