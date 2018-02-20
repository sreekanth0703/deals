# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from deals.models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('post_title',)
    list_display = ('post_title',)
