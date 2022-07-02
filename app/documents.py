from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import log


@registry.register_document
class LogsDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'log_store'

    class Django:
        model = log  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "Receive_Time",
            "Severity",
            "Event_Name",
            "Device",
            "Source",
            "Destination",
            "Action",
            "proto",
            "state",
            "port",
            "is_sm_ips_ports",
            "dwin",
            "dttl",
            "dtcpb",
            "dpkts",
            "dmean",
            "dloss",
            "dbytes",
            "ct_srv_src",
            "ct_srv_dst",
            "ct_src_ltm",
            "ct_src_dport_ltm",
            "ct_dst_src_ltm",
            "ct_dst_sport_ltm",
            "ct_dst_ltm",
            "sbytes",
            "sloss",
            "smean",
            "spkts",
            "stcpb",
            "sttl",
            "swin",
            "rate",
            "ackdat",
            "dinpkt",
            "djit",
            "dload",
            "dur",
            "sinpkt",
            "sjit",
            "sload",
            "synack",
            "tcprtt",
        ]
