from urllib.parse import urlencode

from django.db import IntegrityError
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (
    DetailView, ListView
)
from django.http import (
    JsonResponse, Http404, HttpResponse
)

from utils.constants import (
    C4_ROW_NUMBER, C4_COLUMN_NUMBER, MAX_MOVES_NUMBER
)
from .models import Game, Step


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

        # request user must be one of game players
        if request.user not in [self.object.player_1, self.object.player_2]:
            return redirect("auth:login")

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Get step data. Check if step can be made. If so - make step.
        If not - return JsonResponse with 422 status code. Then check
        if step finished game in win for request user - return JsonResponse with just_won = True
        if step finished game in draw - return JsonResponse with draw = True
        Otherwise render game detail page

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            JsonResponse / HttpResponse  -- response
        """
        self.get(request, *args, **kwargs)

        data = request.POST
        step_x = int(data["x"][0])
        step_y = int(data["y"][0])
        is_correct, errors = Step.check_step(self.object, request.user, step_x)
        if not is_correct:
            return JsonResponse({'errors': errors}, status=422)

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
            request_user {User} -- user that requested to make a move

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


def whether_my_move(request, *args, **kwargs):
    """Return whether requested user should move

    Arguments:
        request {WSGIRequest} -- request

    Raises:
        Http404: if game with given game_pk does not exist

    Returns:
        JsonResponse (JsonResponse) --
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
    except Game.DoesNotExist:
        raise Http404

def game_steps(request, *args, **kwargs):
    """Return steps of game consisting of 'x', 'y', 'user' fields

    Arguments:
        request {WSGIRequest} -- request

    Raises:
        Http404: if game with given game_pk does not exist

    Returns:
        JsonResponse -- list of steps
    """
    game_pk = kwargs['pk']
    try:
        game = Game.objects.get(pk=game_pk)
        steps = game.get_game_steps()
        steps = list(steps.values('x', 'y', 'user'))
        data = {}
        data['steps'] = steps
        data['player_1_pk'] = game.player_1.pk
        data['player_2_pk'] = game.player_2.pk

        return JsonResponse(data)
    except Game.DoesNotExist:
        raise Http404


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
        return result

    def get(self, request, *args, **kwargs):
        """Get search query.
        If it is None - set search query and paginator page url parameters
        and redirect to result page
        Otherwise - render new game page

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponseRedirect / HttpResponse -- response
        """
        query = request.GET.get('q', None)
        if query is None:
            url_reversed = reverse('c4:new-game')
            url_encoded = urlencode({'q': '', 'page': 1})
            return redirect(f"{url_reversed}?{url_encoded}")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create new game and return response with status code

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponse -- HttpResponse with status code
        """
        player_2_username = request.POST['player_2_username']
        player_2 = User.objects.filter(username=player_2_username)[0]
        player_1 = request.user
        game = Game.create(player_1=player_1, player_2=player_2, is_accepted=False)
        status = 200 if game is not None else 400
        return HttpResponse(status=status)


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

    def get(self, request, *args, **kwargs):
        """Get search query.
        If it is None - set search query and paginator page url parameters
        and redirect to result page
        Otherwise - render history page

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponseRedirect / HttpResponse -- response
        """
        query = request.GET.get('q', None)
        if query is None:
            url_reversed = reverse('c4:history')
            # url_encoded = urlencode({'q': 'progress', 'page': 1})
            url_encoded = urlencode({'q': '', 'page': 1})
            return redirect(f"{url_reversed}?{url_encoded}")
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """Accept / decline game and return response with status code

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponse -- HttpResponse with status code
        """
        accept = request.POST.get('accept', None)
        if accept is None:
            status = 400
        else:
            game_pk = request.POST.get('game_pk', None)
            game_pk = int(game_pk) if game_pk is not None else None
            try:
                game = Game.objects.get(pk=game_pk)
                game.set_game_accepted(bool(int(accept[0])))
                status = 200
            except Game.DoesNotExist:
                status = 404
            except IntegrityError:
                status = 400
        return HttpResponse(status=status)
