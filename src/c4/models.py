from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User

from utils.constants import C4_ROW_NUMBER, C4_COLUMN_NUMBER
from .algorithm import check_map


class GameQuerySet(models.QuerySet):
    def search(self, query, *args, **kwargs):
        if query:
            requested_user = kwargs.get('requested_user', None)
            if requested_user:
                ids_list = self.search_by_title(query, requested_user)
                qs = self.filter(
                    Q(player_1__username__icontains=query) |
                    Q(player_2__username__icontains=query) |
                    Q(pk__in=ids_list)
                ).distinct()
                # import pdb
                # pdb.set_trace()
                return qs
            return self
        return self

    def search_by_title(self, query, requested_user):
        ids_list = [game.pk for game in self if query.lower() in game.get_game_status(requested_user).lower()]
        return ids_list


class GameManager(models.Manager):
    def get_queryset(self):
        return GameQuerySet(self.model, using=self._db)

    def search(self, query, *args, **kwargs):
        print('Manager')
        return self.get_queryset().search(query, *args, **kwargs)


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
        return f'Game#{self.pk} - {self.player_1.username} vs {self.player_2.username}. Accepted - {self.is_accepted} '

    @property
    def moves_number(self):
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

    def get_step_map(self):
        #TODO - enum на значення карти
        """Return map of steps of the current game.

        Map values:
            0 - cell is empty
            1 - player_1's move
            2 - player_2's move
            3 - winner's move

        Returns:
            list -- matrix of steps (map)
        """
        steps = Step.objects.filter(game=self)
        map_n = C4_ROW_NUMBER
        map_m = C4_COLUMN_NUMBER
        step_map = [[0 for _ in range(map_m)] for _ in range(map_n)]
        for step in steps:
            step_map[step.y-1][step.x-1] = 1 if step.user == self.player_1 else 2
        is_won, map = check_map(step_map)
        if is_won and not self.end_datetime:
            self.end_datetime = datetime.now() + timedelta(hours=2)
            self.winner = steps.last().user
            self.save()
        return map

    def get_turn_user(self):
        #TODO - docstring
        """[summary]

        Returns:
            [type] -- [description]
        """
        last_user = Step.object.filter(game=self).user
        return self.player_1 if last_user == self.player_2 else self.player_2

    def get_game_status(self, request_user):
        #TODO - docstring
        if not self.is_accepted and self.end_datetime:
            if self.player_1 == request_user:
                return "Rejected"
            elif self.player_2 == request_user:
                return "Declined"
        elif not self.is_accepted and not self.end_datetime:
            if self.player_1.username == request_user.username:
                return "Waiting"
            elif self.player_2.username == request_user.username:
                return "Accept"
        elif not self.winner:
            return "In Progress"
        elif request_user == self.winner:
            return "Won"
        else:
            return "Lost"
    
    def get_game_steps(self):
        #TODO - docstring
        return Step.objects.filter(game=self)


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
    def check_step(game, request_user, step_x, step_y):
        """Check whether step may be made

        Arguments:
            game {Game} --
            request_user {django.contrib.auth.models.User} -- user that requested to make a move
            step_x {int} -- step's x
            step_y {int} -- step's y

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
