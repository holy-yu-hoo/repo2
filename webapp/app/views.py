from django.shortcuts import render


# Create your views here.

def index(request):
	return render(request, 'index.html', context = {'value': '123456'})

# def page(request):
# 	return render()
