from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from .models import ExtendedUser
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    template_name = 'auth/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('sdf')
            else:
                return render(request, self.template_name, context={'form': form, 'error': 'invalid'})


class SignupView(View):
    template_name = 'auth/signup.html'
    success_template_name = 'auth/signup-success.html'
    form = SignupForm

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        extended_user = ExtendedUser.objects.get(user=request.user)
        extended_user.generate_verification_email(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.form(request.POST)
        context['form'] = form
        if form.is_valid():
            password = form['password1'].value()
            username = form['username'].value()
            email = form['email'].value()
            first_name = form['first_name'].value()
            last_name = form['last_name'].value()

            user = User(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )
            user.save()

            context['username'] = username
            extended_user = ExtendedUser(user=user)
            extended_user.save()
            extended_user.generate_verification_email(request)
            return render(request, self.success_template_name, context)
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class VerifyEmailView(View):
    success_template = 'auth/activation/success.html'
    fail_template = 'auth/activation/fail.html'

    def get(self, request, *args, **kwargs):
        try:
            extended_user = ExtendedUser.objects.get(email_auth_token=kwargs['token'])
        except ExtendedUser.DoesNotExist:
            return render(request, self.fail_template, context={'error': 'invalid'})
        responce = extended_user.is_token_valid(kwargs['token'])
        if responce['valid']:
            extended_user.email_auth_token = None
            extended_user.save()
            return render(request, self.success_template)

        else:
            context = {'error': responce['error']}
            return render(request, self.fail_template, context)


# todo: resend verification email view

class ResendVerifictaionEmailView(View):
    form = LoginForm
    template_name = 'auth/activation/resend.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, self.template_name, context={'form': form, 'error': 'invalid'})
            if user.is_active:
                return render(request, self.template_name, context={'form': form, 'active': True})

            extended_user = ExtendedUser.objects.get(user=user)
            extended_user.generate_verification_email(request)
            return HttpResponse('Verification email has been sent')
        return render(request, self.template_name, context={'form': form})
