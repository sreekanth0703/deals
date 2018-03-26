# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100, db_index=True)
    post_desc = models.TextField(default='')
    #deal_type = models.CharField(max_length=100, default='',null=True, db_index=True)
    post_image = models.CharField(max_length=256, default='')
    status = models.IntegerField(default = 1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'POST'

    def __unicode__(self):
        return str(self.post_title)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, null=True, blank=True, default=None, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=350, db_index=True)
    product_url = models.CharField(max_length=350, default='')
    product_image = models.CharField(max_length=256, default='')
    product_category = models.CharField(max_length=64, db_index=True, default='')
    product_price = models.FloatField(default = 0)
    product_mrp = models.FloatField(default = 0)
    offer_start = models.DateTimeField(default=None)
    offer_end = models.DateTimeField(default=None)
    deal_site = models.CharField(max_length=64, db_index=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PRODUCT'
        unique_together = ('post', 'product_name')


class ProductData(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, blank=True, default=None, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64, db_index=True)
    column_value = models.CharField(max_length=120, db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PRODUCT_DATA'
        unique_together = ('product', 'display_name')
