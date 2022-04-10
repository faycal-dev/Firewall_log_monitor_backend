from attr import fields
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Q
from app.documents import LogsDocument
from .serializers import LogsSerializer
# from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
# from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAdminUser, IsAuthenticated, SAFE_METHODS


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
                {"@timestamp": {"order": "desc"}})[0:100]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializedResult = self.logs_serializer(results, many=True)

            return self.get_paginated_response(serializedResult.data)
        except Exception as e:
            return HttpResponse(e, status=500)
