from django.urls import include, path
from django.views.generic import TemplateView

from .views import (
    UserNewGameListView, GameDetailView,
    GameHistoryListView, whether_my_move, game_steps
)

app_name='c4'

urlpatterns = [
    path('', TemplateView.as_view(template_name="c4/home.html"), name='home'),
    path('rules/', TemplateView.as_view(template_name="c4/rules.html"), name='rules'),
    path('new-game/', UserNewGameListView.as_view(), name='new-game'),
    path('history/', GameHistoryListView.as_view(), name='history'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game'),
    path('game/<int:pk>/my_move/', whether_my_move),
    path('game/<int:pk>/steps/', game_steps),
]
