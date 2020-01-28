from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, DetailView, ListView
)
from django.http import (
    JsonResponse, HttpResponseNotFound, HttpResponseRedirect
)

from utils.constants import C4_ROW_NUMBER, C4_COLUMN_NUMBER
from .models import Game, Step
from .forms import GameForm


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
        context['map'] = self.object.get_step_map()
        context['turn_username'] = self.get_turn_username(self.request.user)
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
        is_correct, errors = Step.check_step(self.object, request.user, step_x, step_y)
        if not is_correct:
            return JsonResponse({'errors': errors})

        Step.create(self.object, request.user, step_x, step_y)

        context = self.get_context_data()
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
        last_turn_user = Step.objects.all().last().user
        p_1 = self.object.player_1
        p_2 = self.object.player_2
        turn_user = p_2 if last_turn_user == p_1 else p_1
        return 'Your' if turn_user == request_user else turn_user.username


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
        last_user = Step.objects.filter(game=game).last().user
        my_move = request.user != last_user
        return JsonResponse({'my_move': my_move})
    except User.DoesNotExist:
        return HttpResponseNotFound('<h1>Not Found</h1>')


class UserNewGameListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name="c4/new_game.html"
    paginate_by = 7

    def get_queryset(self):
        query = super().get_queryset()
        result = query.exclude(pk=self.request.user.pk)
        q = self.request.GET.get('q', None)
        if q: result = result.filter(username__icontains=q)
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
        status = None
        if Game.create(player_1=player_1, player_2=player_2, is_accepted=False):
            status = True
        else: status = False
        return JsonResponse({'status': status})
