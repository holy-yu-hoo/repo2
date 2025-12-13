from django.contrib import admin
from . import models


# Register your models here.


class UserProfileInline(admin.TabularInline):
	model = models.UserProfile
	can_delete = False
	verbose_name = "Profile"
	verbose_name_plural = 'Profiles'
	fields = ('name', 'surname', 'about')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("login", "get_name", "get_surname")
	inlines = (UserProfileInline,)
	fields = ('login',)
	verbose_name = 'User'
	verbose_name_plural = 'Users'

	@admin.display(description = 'Name')
	def get_name(self, obj):
		return obj.profile.name

	@admin.display(description = 'Surname')
	def get_surname(self, obj):
		return obj.profile.surname
# fields = ("login", "profile__name", "profile__surname", "profile__about")
