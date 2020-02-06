from jwt import ExpiredSignatureError

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .forms import RegisterForm
from .utils import decode_token, send_activation_email


class RegisterCreateView(CreateView):
    form_class = RegisterForm
    template_name = "authentication/register.html"
    success_url = '/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("c4:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.request.session['activation_token_sent'] = True
        return super().form_valid(form)


def activate_user(request, token=None):
    """Activate user by token

    Arguments:
        request {WSGIRequest} -- request

    Keyword Arguments:
        token {str} -- activation token (default: {None})

    Returns:
        HttpResponseRedirect -- redirect to another page
    """
    if token is not None:
        try:
            decoded_data = decode_token(token, verify=True)
        except ExpiredSignatureError:
            return redirect(reverse('auth:token-expired', args=[token]))

        user = get_object_or_404(User, username=decoded_data['username'])
        if not user.is_active:
            user.is_active = True
            user.save()
        return redirect(reverse("auth:login"))
    return redirect(reverse("c4:home"))


class TokenExpiredView(TemplateView):
    template_name = "authentication/token-expired.html"

    def get(self, request, *args, **kwargs):
        """Decode token, get user.
        If user isn't in db (inactive users can be deleted) redirect to account-expired page
        If user from token or user from request is active - redirect to login page
        Otherwise render token-expired page

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponse / HttpResponseRedirect -- token-expired page or redirect to another page
        """
        super().get(request, *args, **kwargs)
        context = self.get_context_data(token=kwargs['token'])

        token = context['token']
        decoded_data = decode_token(token, verify=False)
        username = decoded_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('auth:account-expired')

        if user.is_active or request.user.is_active:
            return redirect('auth:login')

        context['user'] = user
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Resend activation token if token exists and isn't in request.session expired-token list

        Arguments:
            request {WSGIRequest} -- request

        Returns:
            HttpResponse -- response with status
        """
        token = kwargs.get('token', None)
        if request.session.get('expired_tokens', None) is None:
            request.session['expired_tokens'] = []

        if token is not None and token not in request.session['expired_tokens']:
            username = request.POST.get('username', None)
            user = get_object_or_404(User, username=username)
            send_activation_email(user)

            request.session['expired_tokens'].append(token)
            request.session.modified = True
            return HttpResponse(status=200)
        return HttpResponse(status=400)
