from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

class Game(models.Model):
    # id = models.AutoField(primary_key=True)
    player_1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='player_1',
        null=True
    )
    player_2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='player_2',
        null=True
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='winner',
        null=True
    )
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f'Game#{self.pk} - {self.player_1.name} vs {self.player_2.name}'

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"pk": self.pk})


class Step(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __str__(self):
        return f'Game#{self.game.pk}: step#{self.pk} by {self.user.name} in [{self.x}, {self.y}]'

    def get_absolute_url(self):
        return reverse("step_detail", kwargs={"pk": self.pk})
