from django.urls import include, path

from .views import (
    HomeView,    
)

app_name='c4'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('logout', RegisterView.as_view(), name='logout'),
]
