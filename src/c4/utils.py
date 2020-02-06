from django.db import models
from django.db.models import Q


class GameQuerySet(models.QuerySet):
    def search(self, query, **kwargs):
        """Filter queryset by query

        Arguments:
            query {str} -- search query

        Returns:
            QuerySet -- filtered query set
        """
        result = self
        if query:
            requested_user = kwargs.get('requested_user', None)
            if requested_user:
                ids_list = self.get_game_ids_by_status(query, requested_user)
                qs = self.filter(
                    Q(player_1__username__icontains=query) |
                    Q(player_2__username__icontains=query) |
                    Q(pk__in=ids_list)
                ).distinct()
                result = qs
        return result

    def get_game_ids_by_status(self, query, user):
        """Return ids of games status of which for given user contains query

        Arguments:
            query {str} -- search query
            user {User} -- user

        Returns:
            list -- list of game ids
        """
        ids_list = [game.pk for game in self if query.lower() in game.get_game_status(user).lower()]
        return ids_list


class GameManager(models.Manager):
    def get_queryset(self):
        return GameQuerySet(self.model, using=self._db)

    def search(self, query, *args, **kwargs):
        # print('Manager')
        return self.get_queryset().search(query, *args, **kwargs)
