from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import CreateView #, FormView
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth import login as auth_login

from .forms import RegisterForm


class RegisterCreateView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = '/auth/login/'
    success_message = "Your user account was created successfully." #Please check your email."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        # print(context['form'].errors.items())
        # print(context['form']['password2'].errors)
        return context

    def dispatch(self, *args, **kwargs):
        print('dispatch')
        print(self)
        print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            return HttpResponseRedirect("/home/")
        return super().dispatch(*args, **kwargs)


# class LoginCreateView(SuccessMessageMixin, FormView):
#     form_class = LoginForm
#     template_name = "authentication/login.html"
#     success_url = '/auth/register/'
#     success_message = "Log in successful." #Please check your email."

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # print(context)
#         # print(context['form'].errors.items())
#         # print(context['form']['password2'].errors)
#         return context
    
#     def form_valid(self, form):
#         """Security check complete. Log the user in."""
#         auth_login(self.request, form.get_user())
#         return HttpResponseRedirect(self.get_success_url())

#     # def dispatch(self, *args, **kwargs):
#     #     print('dispatch')
#     #     # if self.request.user.is_authenticated():
#     #     #     return redirect("/")
#     #     return super().dispatch(*args, **kwargs)
