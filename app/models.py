from django.db import models

# Create your models here.
class logs(models.Model):
    id = models.TextField(primary_key=True)
    Receive_Time = models.CharField(max_length=100)
    Severity = models.CharField(max_length=100)
    Event_Type_ID = models.CharField(max_length=100)
    Event_Name = models.CharField(max_length=100)
    Device = models.CharField(max_length=100)
    Source = models.CharField(max_length=100)
    Source_Service = models.CharField(max_length=100)
    Destination = models.CharField(max_length=100)
    Destination_Service = models.CharField(max_length=100)
    Action = models.CharField(max_length=100)
    Description = models.TextField()
    Event_ID = models.CharField(max_length=100)
    

    def __str__(self):
        return self.Event_Type_ID