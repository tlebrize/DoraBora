from django.db import models


class Server(models.Model):
    class ServerStates(models.TextChoices):
        OFFLINE = "offline"
        ONLINE = "online"
        MAINTENANCE = "maintenance"

    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    host = models.CharField(max_length=255, blank=False, null=False)
    port = models.IntegerField(null=False)
    state = models.CharField(max_length=255, choices=ServerStates, null=False, blank=False)
    subscriber_only = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"{self.name} - ({self.host}:{self.port}/)"
