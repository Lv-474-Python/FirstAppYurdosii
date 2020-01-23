from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Game(models.Model):
    """
        Model representing a game history item of 2 players
    """
    player_1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='game_player_1',
        null=True
    )
    player_2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='game_player_2',
        null=True
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='game_winner',
        null=True
    )
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    # Metadata
    class Meta:
        ordering = ['-pk']
        verbose_name = "Game"
        verbose_name_plural = "Games"

    # Methods
    def get_absolute_url(self):
        """
            Returns the url to access a particular instance of Game
        """
        return reverse("game_detail", kwargs={"pk": self.pk})
   
    def __str__(self):
        """
            String for representing the Game object
        """
        return f'Game#{self.pk} - {self.player_1.name} vs {self.player_2.name}'


class Step(models.Model):
    """
        Model representing a step in game made by used
    """
    # Fields
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='steps',
        null=True
    )
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()

    # Metadata
    class Meta:
        verbose_name = "Step"
        verbose_name_plural = "Steps"
    
    # Methods
    def get_absolute_url(self):
        """
            Returns the url to access a particular instance of Step
        """
        return reverse("step_detail", kwargs={"pk": self.pk})

    def __str__(self):
        """"
            String for representing the Step object
        """
        return f'Game#{self.game.pk}: step#{self.pk} by {self.user.name} in [{self.x}, {self.y}]'
