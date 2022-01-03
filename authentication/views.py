from django.shortcuts import render
from django.views import View
from .forms import SignupForm

class SignupView(View):
    template_name = 'auth/signup.html'
    form = SignupForm
    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass
