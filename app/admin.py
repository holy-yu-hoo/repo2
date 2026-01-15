from django.contrib import admin
from .models import Universe, Character, Data
from django import forms
from django.db import models


# Register your models here.

class DataForm(forms.ModelForm):
	model = Data
	fields = '__all__'
	file = forms.FileField(allow_empty_file = True)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
	list_display = ('name', 'file')
	form = DataForm
