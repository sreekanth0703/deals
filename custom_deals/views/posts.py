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
def get_logo_url():
	return "/static/custom_deals/img/logo.png"

def get_paginated_data(tot_data, page_no=1):
	paginator = Paginator(tot_data, 6)
	pagination_data = paginator.page(page_no)
	return pagination_data

def get_posts(self):
	post_objs = Post.objects.filter().order_by('-updation_date')
	pagination_data = get_paginated_data(post_objs, page_no=1)
	posts = PostSerializer(pagination_data.object_list, many=True)
	data = {'json_data': posts.data, 'pagination_data': pagination_data}
	return data

class display_posts(View):
	"""docstring for  display_posts"""
	api_view = ['GET', 'POST']

	def post(self, request):
		limit = int(request.POST.get('limit', 6))
		json_data = get_posts(limit)
		return render(request, 'index_single_post.html', {'json_data': json_data['json_data'],
		 'pagination_data': json_data['pagination_data']})


class all_posts(View):
	def get(self, request, *args, **kwargs):
		json_data = get_posts(self)
		return render(request, 'deals.html', {'json_data': json_data['json_data'], 'logo_url': get_logo_url(),
			'pagination_data': json_data['pagination_data']})