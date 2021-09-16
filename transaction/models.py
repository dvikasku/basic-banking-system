from django.db import models
from django.utils.timezone import now

# Create your models here.
class Payment(models.Model):
    frm = models.CharField(max_length=50)
    to = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.frm} to {self.to}"