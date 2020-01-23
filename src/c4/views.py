from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = "c4/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

# class RulesView(TemplateView):
#     template_name = "c4/rules.html"
