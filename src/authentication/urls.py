from django.urls import include, path
from django.contrib.auth.views import LoginView

from .views import RegisterCreateView

app_name='authentication'

urlpatterns = [
    path('signup/', RegisterCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name= 'authentication/login.html', redirect_authenticated_user=True), name='login'),
    # path('logout', RegisterView.as_view(), name='logout'),
]
