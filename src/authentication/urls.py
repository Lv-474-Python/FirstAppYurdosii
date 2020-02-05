from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import RegisterCreateView, activate_user, TokenExpiredView

app_name='authentication'

urlpatterns = [
    path('signup/', RegisterCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name= 'authentication/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account-expired/', TemplateView.as_view(template_name="authentication/account-expired.html"), name='account-expired'),
    path('activate/<str:token>', activate_user, name='activation'),
    path('activate/<str:token>/expired', TokenExpiredView.as_view(), name='token-expired'),
]
