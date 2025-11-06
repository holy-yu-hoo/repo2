from django.contrib import admin
from . import models
from . import forms
from django.db.models import QuerySet
from . import admin_actions
import typing


@admin.register(models.Universe)
class AdminUniverse(admin.ModelAdmin):
	list_display = ("title", "autor")
	empty_value_display = "[DATA EXPUNGED]"


@admin.register(models.Character)
class AdminCharacter(admin.ModelAdmin):
	list_display = ("name", "universe", "canonic")
	list_editable = ("canonic",)

	@admin.action(description = "invert canonic")
	def toggle_canonic(self, request: typing.Any, queryset: QuerySet):
		self.message_user(request, "DONE")

	def get_actions(self, request):
		actions = super().get_actions(request)
		if request.user.username == "YH":
			print(actions)
			del actions["toggle_canonic"]
		return actions

	actions = (toggle_canonic,)
