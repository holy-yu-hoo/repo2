from django.template.library import Library


register = Library()

@register.filter()
def formatstring(value, arg: str) -> str:
	"""
	use str.format(**value) for dict-like
	use str.format(*value) for tuple-like
	use str.format(value) for simple
	"""
	if hasattr(value, 'keys') and hasattr(value, '__getitem__'):  # dict-like
		result = arg.format(**value)
	elif hasattr(value, '__iter__') and not isinstance(value, str):  # tuple-like
		result = arg.format(*value)
	else:  # simple
		result = arg.format(value)
	return result
