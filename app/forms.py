from django import forms
from django.forms import widgets
from . import models
from . import validators
from django.contrib.auth.forms import AuthenticationForm


class _TextInput(widgets.TextInput):
	base_attrs = {'autocomplete': 'off'}
	
	def __init__(self, attrs: dict = None):
		attrs = attrs.copy() if attrs is not None else {}
		attrs.update(self.base_attrs)
		super().__init__(attrs)


class LoginForm(AuthenticationForm):
	template_name = 'app/forms/form_template.html'
	username = forms.CharField(
		label = 'username',
		widget = _TextInput(attrs = {'class': 'form-control', 'id': 'username', 'placeholder': 'username', }),
		template_name = "app/forms/field.html",
		# validators = (
		# 	validators.CountPatternValidateGE(pattern = 'a', limit_value = 3),
		# 	validators.CountPatternValidateGE('b', 2),
		# 	validators.CountPatternValidateGE(r'\d', 4),
		# ),
		
		label_suffix = '',
	
	
	)
	password = forms.CharField(label = 'password',
		widget = _TextInput(attrs = {'class': 'form-control', 'placeholder': 'username', }),
		label_suffix = '',
		template_name = "app/forms/field.html",
		# validators = (
		# 	validators.CountPatternValidateGE(pattern = 'a', limit_value = 3),
		# 	validators.CountPatternValidateGE('b', 2),
		# 	validators.CountPatternValidateGE(r'\d', 4),
		# ),
	)
	
	
	class Media:
		css = {'all': ('app/css/form.css',)}
