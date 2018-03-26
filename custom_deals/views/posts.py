# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views import View
from rest_framework.renderers import JSONRenderer
from deals.models import *
from custom_deals.serializers import *
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

class display_posts(View):
	"""docstring for  display_posts"""
	api_view = ['GET', 'POST']

	def post(self, request):
		limit = int(request.POST.get('limit', 6))
		post_objs = Post.objects.filter().order_by('-updation_date')
		json_data = []
		for post_obj in post_objs:
			post = PostSerializer(post_obj)
			json_data.append(post.data)
		return render(request, 'index_single_post.html', {'json_data': json_data[:limit]})


class all_posts(View):
	def get(self, request):
		return HttpResponse("Success")
