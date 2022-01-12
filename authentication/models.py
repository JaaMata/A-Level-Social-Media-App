from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
from hashlib import blake2b
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone


class ExtendedUser(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    email_auth_token = models.CharField(max_length=200, null=True, blank=True)
    email_verification_expire_time = models.DateTimeField(null=True)
    password_reset_auth_token = models.CharField(max_length=200, blank=True)

    def generate_token(self):
        # Generates token by combining username, email, id and current time then hashes them using blake2b
        token = bytes(str(self.user.username) + str(self.user.email) + str(self.user.id) + str(timezone.now()), 'utf-8')
        hashed_token = blake2b(token).hexdigest()
        return hashed_token

    def generate_verification_email(self, request):
        # Call the generate token function
        self.email_auth_token = self.generate_token()
        self.save()

        # Generates email content
        authenication_url = f'{get_current_site(request)}/auth/verify-email/{self.email_auth_token}'
        html_content = render_to_string('auth/verify_email.html',
                                        {'username': self.user.username, 'authenication_url': authenication_url})
        text_content = strip_tags(html_content)

        # Generates the expiry time
        self.email_verification_expire_time = timezone.now() + timezone.timedelta(minutes=30)
        self.save()

        # Sends the verification email

        email = EmailMultiAlternatives(
            subject='Verify Your Email',
            body=text_content,
            from_email=None,
            to=[self.user.email])
        email.send()

    def is_token_valid(self, token):
        if self.user.is_active:
            # Returns false if the user is already active
            return {'valid': False, 'error': 'active'}

        if self.email_verification_expire_time < timezone.now():
            # Returns false if the token has expired
            return {'valid': False, 'error': 'expired'}

        if self.email_auth_token == token:
            # If token is valid then if set is_active to true allowing user to login

            user = self.user
            user.is_active = True
            user.save()
            return {'valid': True}

        # todo: Check time is valid, return true is all is met else false the handle false return on view and return render failular template with appropirate error code for user knowlage
