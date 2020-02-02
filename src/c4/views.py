from datetime import datetime, timedelta

from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render
from django.utils.timezone import get_current_timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, DetailView, ListView
)
from django.http import (
    JsonResponse, HttpResponseNotFound, HttpResponseRedirect
)

from utils.constants import (
    C4_ROW_NUMBER, C4_COLUMN_NUMBER, MAX_MOVES_NUMBER
)
from .models import Game, Step


class HomeView(TemplateView):
    template_name = "c4/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'c4/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rows'] = range(C4_ROW_NUMBER)
        context['columns'] = range(C4_COLUMN_NUMBER)
        context['map'] = self.object.get_game_map()
        context['turn_username'] = self.get_turn_username(self.request.user)
        context['MAX_MOVES_NUMBER'] = MAX_MOVES_NUMBER
        return context

    def get(self, request, *args, **kwargs):
        # get_context_data is called by super().get()
        super(GameDetailView, self).get(request, *args, **kwargs)

        if request.user not in [self.object.player_1, self.object.player_2]:
            return HttpResponseRedirect(reverse("auth:login"))
        # sessions об'єкт подивитися

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)

        data = request.POST
        step_x = int(data["x"][0])
        step_y = int(data["y"][0])
        is_correct, errors = Step.check_step(self.object, request.user, step_x)
        if not is_correct:
            return JsonResponse({'errors': errors})

        Step.create(self.object, request.user, step_x, step_y)

        # check if game has just ended
        end_datetime_before = self.object.end_datetime
        context = self.get_context_data()
        end_datetime_after = self.object.end_datetime
        if end_datetime_before != end_datetime_after:
            if request.user == self.object.winner:
                return JsonResponse({'just_won': True})
            return JsonResponse({'draw': True})

        return render(request, self.template_name, context)

    def get_turn_username(self, request_user):
        """Get current turn user username

        Arguments:
            request_user {django.contrib.auth.models.User} -- user that requested to make a move

        Returns:
            string --
                'Your' - if requested_user equals to user that has to move,
                current turn user username - otherwise
        """
        p_1 = self.object.player_1
        p_2 = self.object.player_2

        steps = self.object.get_game_steps()
        if not steps:
            if request_user == p_1:
                return "Your"
            return p_1.username

        turn_user = p_2 if steps.last().user == p_1 else p_1
        return 'Your' if turn_user == request_user else turn_user.username

    def set_context_win(self, context):
        game = self.object
        context['player_1_endgame'] = ' player-3' if game.player_1 == game.winner else ''
        context['player_2_endgame'] = ' player-3' if game.player_2 == game.winner else ''
        return context


def whether_my_move(request, *args, **kwargs):
    """Return whether requested user should move

    Arguments:
        request {WSGIRequest} -- request

    Returns:
        dict (JsonResponse) --
            my_move (bool) - whether requested user should move
    """
    game_pk = kwargs['pk']
    try:
        game = Game.objects.get(pk=game_pk)
        steps = game.get_game_steps()
        if not steps:
            my_move = request.user == game.player_1
        else:
            last_user = steps.last().user
            my_move = request.user != last_user
        return JsonResponse({'my_move': my_move})
    except User.DoesNotExist:
        return HttpResponseNotFound('<h1>Not Found</h1>')


class UserNewGameListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = "c4/new_game.html"
    paginate_by = 7
    ordering = ['username']

    def get_queryset(self):
        qs = super().get_queryset()
        result = qs.exclude(pk=self.request.user.pk)
        query = self.request.GET.get('q', None)
        if query:
            result = result.filter(username__icontains=query)
        # import pdb
        # pdb.set_trace()
        return result

    def post(self, request, *args, **kwargs):
        """Post request for creating new game

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            JsonResponse -- JsonResponse with status (whether post request was successful)
        """
        player_2_username = request.POST['player_2_username']
        player_2 = User.objects.filter(username=player_2_username)[0]
        player_1 = request.user
        status = bool(Game.create(player_1=player_1, player_2=player_2, is_accepted=False))
        return JsonResponse({'status': status})


class GameHistoryListView(LoginRequiredMixin, ListView):
    model = Game
    context_object_name = 'games'
    template_name = "c4/history.html"
    paginate_by = 4

    def get_queryset(self):
        qs = self.get_queryset_by_user()
        query = self.request.GET.get('q', None)
        if query:
            qs = qs.search(query, requested_user=self.request.user)
        return qs

    def get_queryset_by_user(self):
        return super().get_queryset().filter(
            Q(player_1=self.request.user) |
            Q(player_2=self.request.user)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_games'] = self.get_queryset_by_user()
        return context

    def post(self, request, *args, **kwargs):
        """Post request for accept / decline game

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            JsonResponse -- JsonResponse with status (whether post request was successful)
        """
        accept = request.POST.get('accept', None)
        if accept is None:
            status = False
        else:
            game_pk = int(request.POST['game_pk'])
            game = Game.objects.get(pk=game_pk)
            timezone = get_current_timezone()
            accept = bool(int(accept[0]))
            game.is_accepted = accept
            game.start_datetime = datetime.now(tz=timezone) + timedelta(hours=2)
            if not accept:
                game.end_datetime = datetime.now(tz=timezone) + timedelta(hours=2)
            try:
                game.save()
                status = True
            except IntegrityError:
                status = False
        return JsonResponse({'status': status})
