from django.contrib.auth.models import AbstractUser
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length = 60)
    time = models.DateTimeField()
    place = models.CharField(max_length = 180)
    code = models.CharField(max_length = 20, blank=True)
    points = models.IntegerField(default = 0)
    descriptions = models.TextField(blank=True)

    class Meta:
        ordering = ('time',)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    points = models.IntegerField(default = 0)
    events = models.ManyToManyField(Event, related_name="user_list", blank=True)
    organization = models.CharField(max_length = 80)

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return self.email

    def calc_points(events):
        for event in events:
            total=+event.points

