from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    event_completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("calendarwithevent:event-update", args=[self.id])

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.title} {self.start_date} ~ {self.end_date}, Completed: {self.event_completed}"