from django.shortcuts import render, redirect, reverse


def index(request):
	return redirect(reverse("main:index"))
