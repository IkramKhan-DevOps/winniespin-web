from django.shortcuts import render, redirect
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = 'website/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        return redirect("accounts:cross-auth")


