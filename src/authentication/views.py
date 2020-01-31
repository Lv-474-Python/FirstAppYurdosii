from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterCreateView(CreateView):
    form_class = RegisterForm
    template_name = "authentication/register.html"
    success_url = '/auth/login/'
    success_message = "Your user account was created successfully." #Please check your email."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)
