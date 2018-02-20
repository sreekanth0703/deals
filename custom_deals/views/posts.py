# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from deals.models import *
from custom_deals.serializers import *
import json

# Create your views here.

def display_posts(request):
    post_objs = Post.objects.filter()
    json_data = []
    for post_obj in post_objs:
        post = PostSerializer(post_obj)
        json_data.append(post.data)
    return HttpResponse(json.dumps({'data': json_data}))