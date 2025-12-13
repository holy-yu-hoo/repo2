# forms.py
from django import forms

from .models import User


class UserRegistrationForm(forms.ModelForm):
	template_name = "main/forms/user_registration.html"
	form_name = "Registration"

	login = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-field'}), label = 'Login')

	password = forms.CharField(
		widget = forms.PasswordInput(attrs = {'class': 'form-field'}),
		label = "Password",
	)

	password_confirm = forms.CharField(
		widget = forms.PasswordInput(attrs = {'class': 'form-field'}),
		label = "Confirm Password",
	)


	class Meta:
		model = User
		fields = ['login', 'password']


	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password")
		password_confirm = cleaned_data.get("password_confirm")

		if password != password_confirm:
			self.add_error('password_confirm', "Passwords do not match")

		return cleaned_data

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password"])

		if commit:
			user.save()
		return user

	@property
	def user(self):
		try:
			user = self.Meta.model.objects.get(login = self.cleaned_data["login"])
		except self.Meta.model.DoesNotExist:
			raise self.Meta.model.DoesNotExist("There is no user with this login")
		else:
			return user


class UserLoginForm(forms.Form):
	template_name = "main/forms/user_registration.html"
	form_name = "Login"

	login = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-field'}), label = 'Login')

	password = forms.CharField(
		widget = forms.PasswordInput(attrs = {'class': 'form-field'}),
		label = "Password",
	)


	class Meta:
		model = User
		fields = ['login', 'password']


	def clean(self):
		cleaned_data = super().clean()

		try:
			user = self.Meta.model.objects.get(login = self.cleaned_data["login"])
		except self.Meta.model.DoesNotExist:
			self.add_error('login', "There is no user with this login")
		else:
			if not user.check_password(self.cleaned_data["password"]):
				self.add_error('password', "Password is incorrect")

		return cleaned_data

	@property
	def user(self):
		try:
			user = self.Meta.model.objects.get(login = self.cleaned_data["login"])
		except self.Meta.model.DoesNotExist:
			raise self.Meta.model.DoesNotExist("There is no user with this login")
		else:
			return user
