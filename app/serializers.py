from rest_framework import serializers
from app.models import log, matrice


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = log
        fields = (

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
        )


class MatriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = matrice
        fields = ("data", "groupeByValue", "title", "date")
