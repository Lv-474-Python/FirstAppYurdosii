from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User

from utils.constants import (
    C4_ROW_NUMBER, C4_COLUMN_NUMBER, MAX_MOVES_NUMBER,
    TIME_DELTA_OFFSET
)
from utils.enums import MapValue, GameStatus
from .utils import GameManager
from .algorithm import check_map


class Game(models.Model):
    """
        Model representing a game history item of 2 players
    """
    player_1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='games_p1',
        null=True
    )
    player_2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='games_p2',
        null=True
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='game_winner',
        null=True
    )
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    is_accepted = models.BooleanField(default=False)

    objects = GameManager()

    # Metadata
    class Meta:
        ordering = ['-pk'] # '-end'
        verbose_name = "Game"
        verbose_name_plural = "Games"

    # Methods
    def get_absolute_url(self):
        """Get absolute url to Game object

        Returns:
            string -- the url to access a particular instance of Game
        """
        return reverse("c4:game", kwargs={"pk": self.pk})

    def __str__(self):
        """Return string representing of Game object

        Returns:
            string -- representing of Game object
        """
        return f'Game#{self.pk} - {self.player_1.username} vs ' + \
        f'{self.player_2.username}. Accepted - {self.is_accepted}'

    @property
    def moves_number(self):
        """Return number of this game steps

        Returns:
            int -- moves number
        """
        return self.steps.count()

    @staticmethod
    def create(player_1, player_2, is_accepted):
        """Create new game

        Arguments:
            player_1 {User} -- player_1
            player_2 {User} -- player_2
            is_accepted {bool} -- whether game is accepted by player_2

        Returns:
            Game -- created Game object
        """
        game = Game(player_1=player_1, player_2=player_2, is_accepted=is_accepted)
        try:
            game.save()
            return game
        except IntegrityError:
            return None

    def get_game_map(self):
        """Return map of steps of the current game.

        Returns:
            list -- matrix of steps (map)
        """
        steps = self.get_game_steps()
        map_n = C4_ROW_NUMBER
        map_m = C4_COLUMN_NUMBER
        step_map = [[MapValue.EMPTY for _ in range(map_m)] for _ in range(map_n)]
        for step in steps:
            if step.user == self.player_1:
                step_map[step.y-1][step.x-1] = MapValue.PLAYER_1
            else:
                step_map[step.y-1][step.x-1] = MapValue.PLAYER_2

        is_won, game_map = check_map(step_map)
        if is_won and not self.end_datetime:
            timezone = get_current_timezone()
            self.end_datetime = datetime.now(tz=timezone) + timedelta(hours=TIME_DELTA_OFFSET)
            self.winner = steps.last().user
            self.save()
        elif steps.count() == MAX_MOVES_NUMBER:
            timezone = get_current_timezone()
            self.end_datetime = datetime.now(tz=timezone) + timedelta(hours=TIME_DELTA_OFFSET)
            self.save()

        return game_map

    def get_turn_user(self):
        """Return user that has to move next

        Returns:
            User -- user that has to move next
        """
        last_user = Step.object.filter(game=self).user
        return self.player_1 if last_user == self.player_2 else self.player_2

    def get_game_status(self, request_user):
        """Return game status for user

        Arguments:
            request_user {User} -- user that requested game_status

        Returns:
            str -- game status
        """
        status = GameStatus.LOST
        if not self.is_accepted and self.end_datetime:
            if self.player_1 == request_user:
                status = GameStatus.REJECTED
            else:
                status = GameStatus.DECLINED
        elif not self.is_accepted and not self.end_datetime:
            if self.player_1.username == request_user.username:
                status = GameStatus.WAITING
            else:
                status = GameStatus.ACCEPT
        elif not self.winner:
            if self.moves_number == MAX_MOVES_NUMBER:
                status = GameStatus.DRAW
            else:
                status = GameStatus.PROGRESS
        elif request_user == self.winner:
            status = GameStatus.WON
        return status.value

    def get_game_steps(self):
        """Get steps of particular gam

        Returns:
            QuerySet -- game's steps
        """
        return Step.objects.filter(game=self)

    def set_game_accepted(self, accept):
        """Accept / Decline game

        Arguments:
            accept {bool} -- whether game is accepted
        """
        timezone = get_current_timezone()
        self.is_accepted = accept
        self.start_datetime = datetime.now(tz=timezone) + timedelta(hours=TIME_DELTA_OFFSET)
        if not self.is_accepted:
            self.end_datetime = datetime.now(tz=timezone) + timedelta(hours=TIME_DELTA_OFFSET)
        self.save()


class Step(models.Model):
    """
        Model representing a user's step in game
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
        ordering = ['pk']
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    # Methods
    def __str__(self):
        """Return string representing of Step object

        Returns:
            string -- representing of Step object
        """
        return f'Game#{self.game.pk}: step#{self.pk} by {self.user.username} in [{self.x},{self.y}]'

    @staticmethod
    def create(game, user, step_x, step_y):
        """Create new step

        Arguments:
            game {Game} -- game object
            user {django.contrib.auth.models.User} -- user that made a move
            step_x {int} -- step's x
            step_y {int} -- step's y

        Returns:
            Step -- created step
        """
        qs = Step.objects.filter(game=game, x=step_x)
        step_y = C4_ROW_NUMBER if not qs else qs.last().y - 1
        step = Step(game=game, user=user, x=step_x, y=step_y)
        try:
            step.save()
            return step
        except IntegrityError:
            return None

    @staticmethod
    def check_step(game, request_user, step_x):
        """Check whether step may be made

        Arguments:
            game {Game} --
            request_user {django.contrib.auth.models.User} -- user that requested to make a move
            step_x {int} -- step's x

        Returns:
            tuple(bool, string) --
                bool - whether move may be made
                string - errors
        """
        qs = game.get_game_steps()
        if not qs:
            if request_user != game.player_1:
                return (False, "It isn't your turn to move")
        elif qs.last().user == request_user:
            return (False, "It isn't your turn to move")
        elif qs.filter(x=step_x, y=1):
            return (False, "This column is full already")
        return (True, "")
