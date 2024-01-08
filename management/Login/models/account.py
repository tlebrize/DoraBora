from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Account(models.Model):
    class AccountStates(models.TextChoices):
        OFFLINE = "offline"
        IN_LOGIN = "in_login"
        IN_GAME = "in_game"
        BANNED = "banned"

    class CommunityChoices(models.IntegerChoices):
        ZERO = 0

    dj_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account",
    )
    nickname = models.CharField(max_length=255, unique=True)
    state = models.CharField(
        max_length=255,
        default=AccountStates.OFFLINE,
        choices=AccountStates,
    )
    subscribed_until = models.DateTimeField()
    security_question = models.CharField(
        max_length=511,
        blank=False,
        null=False,
    )
    community = models.IntegerField(
        default=CommunityChoices.ZERO,
        choices=CommunityChoices,
        null=False,
    )
    switch_token = models.CharField(max_length=1023, null=True, default=True)

    def __str__(self):
        return f"{self.nickname} ({self.dj_user})"


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance.dj_user)
