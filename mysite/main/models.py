from django.db import models
from datetime import datetime

# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200, default="Company Name")
    tutorial_content = models.TextField(null=True, blank=True)
    tutorial_published = models.DateTimeField("date published", default=datetime.now)
    tutorial_imageurl = models.CharField(max_length=200, default="static/main/images/no-image.jpg")
    tutorial_has_twitter_data = models.BooleanField(default=False, null=True, blank=True)
    tutorial_link = models.CharField(max_length=200, default="https://en.wikipedia.org/wiki/JetBlue", null=True, blank=True)

    def __str__(self):
        return self.tutorial_title