from django.template.library import Library
from django.template.defaulttags import ForNode
from django import template
import re


register = Library()

class RangeForNode(template.Node):

	def __init__(self, nodelist, loopvars, sequence, *args):
		self.nodelist = nodelist
		self.vars = loopvars
		self.sequence = sequence
		self.args = args

	def __repr__(self):
		return f'<{self.__class__.__name__}>'


	def render(self, context):
		self.args = tuple(arg.resolve(context) for arg in self.args)
		context["range_sequence"] = range(*self.args)
		node = ForNode(self.vars, self.sequence, False, self.nodelist)

		return node.render(context)

@register.tag(name = "rangefor")
def rangefor(parser, token):
	try:
		tag_name, loopvar, _, *args = token.split_contents()
		if len(args) == 0:
			raise ValueError
	except ValueError:
		raise template.TemplateSyntaxError("'rangefor' statements should have three words and at least one arguments: %s" % token.contents)

	nodelist = parser.parse(('endrangefor',))
	parser.delete_first_token()

	args = map(parser.compile_filter, args)
	loopvars = [loopvar]
	sequence = parser.compile_filter("range_sequence")

	return RangeForNode(nodelist, loopvars, sequence, *args, )


class CorrectIndentNode(template.Node):

	def __init__(self, nodelist):
		self.nodelist = nodelist

	def indent_nodelist(self, nodelist, depth = 1):
		for node in nodelist:
			if hasattr(node, "nodelist"):
				if node.nodelist[0].s[0] == '\n':
					self.indent_nodelist(node.nodelist, depth + 1)
			elif hasattr(node, "s"):
				line = node.s
				line = re.sub(r"\n\t+", lambda match: match.group(0)[:-depth], line)
				node.s = line


	def render(self, context):
		self.indent_nodelist(self.nodelist)
		output = self.nodelist.render(context)
		# output = re.sub(r"\n\t*\n", '\n', output)
		return output.strip()

@register.tag(name = "corindent")
def do_correct_indent(parser, token):
	nodelist = parser.parse(('endcorindent',))
	parser.delete_first_token()
	return CorrectIndentNode(nodelist)

@register.simple_tag(name = "br")
def breakline():
	return '\n'
