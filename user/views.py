from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views import generic

from core.models import Scraper

class EmailForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def _post_clean(self):
        super()._post_clean()
        email = self.cleaned_data.get('email')
        if email:
            try:
                User.objects.get(username=email)
                self.add_error('email', 'Such username exists')
            except User.DoesNotExist:
                pass

    def save(self, commit=True):
        try:
            user = User.objects.create_user(self.cleaned_data["email"], self.cleaned_data["email"],
                                            self.cleaned_data['password2'])
            Scraper.objects.create(user=user)
            return user
        except IntegrityError:
            raise forms.ValidationError('Username exists')


class SignUp(generic.CreateView):
    form_class = EmailForm
    template_name = 'signup.html'

    def form_valid(self, form):
        username = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        if form.is_valid():
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                # Scraper.objects.create(user=user)
                login(self.request, user)
                return redirect('home')