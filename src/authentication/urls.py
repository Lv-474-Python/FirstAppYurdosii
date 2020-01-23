from django.urls import include, path
from django.contrib.auth.views import LoginView

from .views import (
    RegisterCreateView,
    # LoginCreateView,
    # LogoutView,
)

app_name='authentication'

urlpatterns = [
    path('signup/', RegisterCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout', RegisterView.as_view(), name='logout'),
]
