from django.db import models
from django_pandas.managers import DataFrameManager


# Create your models here.

class sentimentSentence(models.Model):
    date=models.DateField()
    category=models.CharField(max_length=125, blank=True , null=True)
    sentence=models.TextField()
    sentence_short=models.CharField(max_length=5000, blank=True , null=True)
    sentence_keywords= models.CharField(max_length=3000, blank=True , null=True)
    sentence_sentiment=models.CharField(max_length=3000, blank=True , null=True)
    sentence_sentiment_net=models.FloatField(default=0)
    sentence_sent_score=models.FloatField(default=0)
    sentence_sentiment_label=models.IntegerField(default=1)
    sentence_entities=models.CharField(max_length=3000, blank=True , null=True)
    sentence_non_entities=models.CharField(max_length=3000, blank=True , null=True)

    objects = DataFrameManager()

class young(models.Model):
    date=models.DateField()
    logits=models.FloatField(default=0)
    net_sent=models.FloatField(default=0)
    logits_mean=models.FloatField(default=0)
    net_sent_mean=models.FloatField(default=0)
    MA_logits=models.FloatField(default=0)
    MA_net_sent=models.FloatField(default=0)
    MA_net_sent_ema_alpha_1=models.CharField(max_length=125, blank=True , null=True)
    MA_net_sent_ema_alpha_3=models.CharField(max_length=125, blank=True , null=True)
    MA_net_sent_ema_alpha_5=models.CharField(max_length=125, blank=True , null=True)

    objects = DataFrameManager()


class TimeSeries(models.Model):

    objects = DataFrameManager()
