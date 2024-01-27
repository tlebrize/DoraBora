from django.db import models
from django.utils import timezone


class Account(models.Model):
    class States(models.TextChoices):
        OFFLINE = "offline"
        IN_LOGIN = "in_login"
        IN_GAME = "in_game"
        BANNED = "banned"

    class Communities(models.IntegerChoices):
        ZERO = 0

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=127, null=False, blank=False)
    nickname = models.CharField(max_length=255, unique=True)
    state = models.CharField(
        max_length=255,
        default=States.OFFLINE,
        choices=States,
    )
    subscribed_until = models.DateTimeField()
    security_question = models.CharField(
        max_length=511,
        blank=False,
        null=False,
    )
    community = models.IntegerField(
        default=Communities.ZERO,
        choices=Communities,
        null=False,
    )
    switch_token = models.CharField(max_length=1023, null=False, blank=True, default="")
    is_game_master = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"{self.username} - {self.nickname} ({self.state})"

    def format_is_game_master(self):
        return str(int(self.is_game_master))

    def format_security_question(self):
        return self.security_question.replace(" ", "+")

    def format_subscribed(self):
        if not self.subscribed_until:
            return ""

        return f"{self.subscribed_milliseconds()}|"

    def subscribed_milliseconds(self):
        if not self.subscribed_until:
            return 0
        return max(0, int((self.subscribed_until - timezone.now()).total_seconds()))
