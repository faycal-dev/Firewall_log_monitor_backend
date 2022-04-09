from django.db.models import fields
from rest_framework import serializers
from app.models import logs


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = logs
        fields = (
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
            "Event_ID",)
