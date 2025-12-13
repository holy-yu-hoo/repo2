from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import admin


class User(models.Model):
	login = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)


	class Meta:
		constraints = (
			models.UniqueConstraint(fields = ("login",), name = "unique_login"),
		)


	def set_password(self, raw_password):
		self.password = make_password(raw_password)

	def check_password(self, raw_password):
		return check_password(raw_password, self.password)

	def __str__(self):
		return f"{self.login}"

	__repr__ = __str__

	@admin.display(description = 'Name')
	def profile_name(self):
		return self.profile.name if hasattr(self, 'profile') else '-'

	@admin.display(description = 'Surname')
	def profile_name(self):
		return self.profile.surname if hasattr(self, 'profile') else '-'

	@admin.display(description = 'About')
	def profile_about(self):
		return self.profile.about if hasattr(self, 'profile') else '-'


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name = 'profile', related_query_name = 'profile')
	name = models.CharField(max_length = 200, blank = True, null = True, default = '')
	surname = models.CharField(max_length = 200, blank = True, null = True, default = '')
	about = models.TextField(blank = True, null = True, default = '')


	def __str__(self):
		return f"{self.name} {self.surname}"

	__repr__ = __str__
