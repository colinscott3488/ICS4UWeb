from django.db import models
from django.contrib.auth.models import User
import datetime

class Schedule(models.Model):
    user = models.CharField(max_length=100)
    dateStarting = models.DateField(default=datetime.datetime.now())
    startTime = models.TimeField(default=datetime.datetime.now())
    endTime = models.TimeField(default=datetime.datetime.now())
    jobCode = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.user} ({(self.startTime).strftime("%-I:%M %p")} - {(self.endTime).strftime("%-I:%M %p")} / {self.dateStarting})"

class ShiftMarketplace(models.Model):
    dateStarting = models.DateField(default=datetime.datetime.now())
    startTime = models.TimeField(default=datetime.datetime.now())
    endTime = models.TimeField(default=datetime.datetime.now())
    jobCode = models.CharField(max_length=20)
    shiftID = models.IntegerField(max_length=20)
    def __str__(self):
        return f"({(self.startTime).strftime("%-I:%M %p")} - {(self.endTime).strftime("%-I:%M %p")} / {self.dateStarting})"
    