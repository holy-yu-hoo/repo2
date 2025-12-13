from typing import Callable
import functools
import inspect


class LoginArgumentNotFound(Exception): pass


class PermissionsResolver:
	"""Decorate view function to resolve permissions"""

	def __init__(self, *permissions: str, login_param = 'login'):
		self.permissions = permissions
		self.login_param = login_param
		self.view_func = None

	def __call__(self, view_func):
		"""wraps view func"""

		@functools.wraps(view_func)
		def wrapper(request, *args, **kwargs):
			for permission in self.permissions:
				handler = self.permissions_handlers[permission]
				passed, callback = handler(request, *args, **kwargs)
				if not passed:
					return callback()
			return view_func(request, *args, **kwargs)

		return wrapper


	def get_login(self, *args, **kwargs):
		"""Find login argument"""

		if self.login_param in kwargs:
			return kwargs[self.login_param]
		else:
			sig_params = list(inspect.signature(self.view_func).parameters.keys())

			for i, param_name in enumerate(sig_params[1:], 1):
				if param_name == self.login_param and i - 1 < len(args):
					return args[i - 1]
		raise LoginArgumentNotFound("Login argument not found in arguments and keyword arguments")

	@staticmethod
	def login_check(request, *args, **kwargs):
		"""check authentication"""

		passed = 'user' in request.session
		callback = lambda: redirect('main:login')
		return passed, callback


	def owner_check(self, request, *args, **kwargs):
		"""check authorization"""
		passed, callback = self.login_check(request, *args, **kwargs)
		if not passed:
			return callback()

		login_arg = self.get_login(*args, **kwargs)
		passed = request.session['user']['login'] == login_arg

		callback = lambda: redirect(request.META.get('HTTP_REFERER', reverse('main:index')))

		return passed, callback

	@property
	def permissions_handlers(self) -> dict[str, Callable]:
		return {"login": self.login_check, "owner": self.owner_check}
