from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime
from django.contrib.auth.models import User,Permission,Group
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required as django_login_required
from django.shortcuts import render, redirect
import re
import json

def login_required(f):
    """Login Decorator """
    def wrap(request, *args, **kwargs):
        """ this check the session if userid key exist, if not it will redirect to login page """
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def user_logined(f):
    """Login Check Decorator """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
