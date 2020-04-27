from django.db import models

# Create your models here.

class Tweet(models.Model):
    customer_name = models.CharField(max_length=50, default="Company Name", null=True, blank=True)
    tweet_text = models.CharField(max_length=280)
    tweet_polarity = models.FloatField(null=True, blank=True)
    tweet_subjectivity = models.FloatField(null=True, blank=True)
    tweet_sentiment = models.CharField(max_length=10,null=True, blank=True)