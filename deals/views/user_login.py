# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from deals.views.decorators import login_required, user_logined
import json

@csrf_exempt
@user_logined
def login(request):
    ''' Login Template '''
    return render(request, 'login/login.html')


@csrf_exempt
def member_login(request):
    ''' Login the user '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username and password:
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth_login(request, user)

            return HttpResponse(json.dumps({'status': 1, 'data': {'username': username, 'id': request.user.id}, 'message': 'Success'}))
    return HttpResponse(json.dumps({'status': 0, 'message': 'Username and Password in Not Correct'}))


@csrf_exempt
@login_required
def home(request):
    ''' Dashboard Template '''
    return render(request, 'main/dashboard.html')


@csrf_exempt
def logout(request):
    ''' Logout Template '''
    auth_logout(request)
    return HttpResponse("Successs")
