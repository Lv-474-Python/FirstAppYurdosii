from django.db import models
from django.db.models import Q


class GameQuerySet(models.QuerySet):
    def search(self, query, **kwargs):
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

    def search_by_title(self, query, user):
        ids_list = [game.pk for game in self if query.lower() in game.get_game_status(user).lower()]
        return ids_list


class GameManager(models.Manager):
    def get_queryset(self):
        return GameQuerySet(self.model, using=self._db)

    def search(self, query, *args, **kwargs):
        # print('Manager')
        return self.get_queryset().search(query, *args, **kwargs)
