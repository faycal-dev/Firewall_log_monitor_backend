from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import logs


@registry.register_document
class LogsDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'logs2'
        

    class Django:
        model = logs # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "Receive_Time",
            "Severity",
            "Event_Type_ID",
            "Event_Name",
            "Device",
            "Source",
            "Source_Service",
            "Destination",
            "Destination_Service",
            "Action",
            "Description",
            "Event_ID",
        ]