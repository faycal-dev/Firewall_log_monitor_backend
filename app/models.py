from django.db import models
from django.utils import timezone

# Create your models here.


class log(models.Model):
    # id = models.TextField(primary_key=True, max_length=1000)
    Receive_Time = models.CharField(max_length=100)
    Severity = models.CharField(max_length=100)
    Event_Name = models.CharField(max_length=100)
    Device = models.CharField(max_length=100)
    Source = models.CharField(max_length=100)
    Destination = models.CharField(max_length=100)
    Action = models.CharField(max_length=100)
    proto = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    port = models.IntegerField(default=0)
    is_sm_ips_ports = models.IntegerField(default=0)
    dwin = models.IntegerField(default=0)
    dttl = models.IntegerField(default=0)
    dtcpb = models.IntegerField(default=0)
    dpkts = models.IntegerField(default=0)
    dmean = models.IntegerField(default=0)
    dloss = models.IntegerField(default=0)
    dbytes = models.IntegerField(default=0)
    ct_srv_src = models.IntegerField(default=0)
    ct_srv_dst = models.IntegerField(default=0)
    ct_src_ltm = models.IntegerField(default=0)
    ct_src_dport_ltm = models.IntegerField(default=0)
    ct_dst_src_ltm = models.IntegerField(default=0)
    ct_dst_sport_ltm = models.IntegerField(default=0)
    ct_dst_ltm = models.IntegerField(default=0)
    sbytes = models.IntegerField(default=0)
    sloss = models.IntegerField(default=0)
    smean = models.IntegerField(default=0)
    spkts = models.IntegerField(default=0)
    stcpb = models.IntegerField(default=0)
    sttl = models.IntegerField(default=0)
    swin = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    ackdat = models.FloatField(default=0)
    dinpkt = models.FloatField(default=0)
    djit = models.FloatField(default=0)
    dload = models.FloatField(default=0)
    dur = models.FloatField(default=0)
    sinpkt = models.FloatField(default=0)
    sjit = models.FloatField(default=0)
    sload = models.FloatField(default=0)
    synack = models.FloatField(default=0)
    tcprtt = models.FloatField(default=0)
    
    def __str__(self):
        return self.Receive_Time


class matrice(models.Model):

    date = models.DateTimeField(default=timezone.now)
    groupeByValue = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    data = models.JSONField(default='{}')

    def __str__(self):
        return self.date
