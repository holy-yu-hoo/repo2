from django.core import validators, exceptions
import re
import functools
import collections.abc as annotations
import operator


class CountPatternValidate(validators.BaseValidator):
	"""checking the required number of occurrences of the pattern"""
	
	compare_func: annotations.Callable[[int, int], bool] = None
	
	def __init__(self, pattern: str | re.Pattern[str], limit_value: int, *, compare_func: annotations.Callable[[int, int], bool] = None, message: str = None, ):
		self.pattern = pattern
		
		# Устанавливаем compare_func: сначала из параметра, потом из класса
		self.compare_func = compare_func or self.compare_func
		if not self.compare_func: raise ValueError("compare_func must be defined")
		
		message = message or self.message
		self.message = message.format(pattern = self.pattern)
		
		super().__init__(limit_value, self.message)
	
	def compare(self, a, b):
		return not self.compare_func(a, b)
	
	def clean(self, value):
		return len(re.findall(self.pattern, value))


class CountPatternValidateGE(CountPatternValidate):
	compare_func = operator.ge
	message = "Ensure this string contain «{pattern}» at least %(limit_value)s occurrences."


class CountPatternValidateGT(CountPatternValidate):
	compare_func = operator.gt
	message = "Ensure this string contain «{pattern}» is greater than %(limit_value)s occurrences."


class CountPatternValidateLE:
	compare_func = operator.le
	message = "Ensure this string contain «{pattern}» is less than or equal %(limit_value)s occurrences."


class CountPatternValidateLT:
	compare_func = operator.lt
	message = "Ensure this string contain «{pattern}» is less than %(limit_value)s occurrences."


class CountPatternValidateEQ:
	compare_func = operator.eq
	message = "Ensure this string contain «{pattern}» exactly %(limit_value)s occurrences."


class CountPatternValidateNE:
	compare_func = operator.ne
	message = "Ensure this string not contain «{pattern}» exactly %(limit_value)s occurrences."
