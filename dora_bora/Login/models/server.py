from django.db import models
from django.db.models import Count, Q


class ServerQuerySet(models.QuerySet):
    async def aformat_login_list(self):
        return "|".join([f"{s.id};{s.format_state()};110;0" async for s in self.all()])

    async def format_server_list(self, account_id):
        return "|".join(
            [
                f"{s.id},{s.character_count}"
                async for s in self.annotate(
                    character_count=Count(
                        "characters",
                        filter=Q(characters__account_id=account_id),
                    )
                )
            ]
        )


class Server(models.Model):
    class States(models.TextChoices):
        OFFLINE = "offline"
        ONLINE = "online"
        MAINTENANCE = "maintenance"

    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    host = models.CharField(max_length=255, blank=False, null=False)
    port = models.IntegerField(null=False)
    state = models.CharField(max_length=255, choices=States, null=False, blank=False)
    subscriber_only = models.BooleanField(default=False, null=False)

    objects = ServerQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} - {self.host}:{self.port}"

    def format_state(self):
        if self.state == self.States.OFFLINE:
            return "0"
        elif self.state == self.States.ONLINE:
            return "1"
        elif self.state == self.States.MAINTENANCE:
            return "2"
        else:
            raise Exception(f"Invalid state for {self.id} : {self.state}.")

    def format_connection(self):
        return f"{self.host}:{self.port}"

    async def acharacter_count(self):
        return 1
