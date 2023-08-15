from djongo import models
from djongo.models.fields import ObjectIdField, Field
from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=100, default="")
    receipt = models.CharField(max_length=100, default="")
    receiptAmount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        super(Survey, self).save(*args, **kwargs)
