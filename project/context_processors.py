def context_processor(request):
	return {'data': 'i am data'}


def session(request):
	return {'session': request.session}
