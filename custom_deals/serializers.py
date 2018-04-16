from rest_framework import serializers
from rest_framework import pagination
from deals.models import *


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = ('display_name',)

class ProductSerializer(serializers.ModelSerializer):
    product_data = ProductDataSerializer(source='productdata_set', many=True)

    class Meta:
        model = Product
        fields = ('product_name', 'product_data')

class PostSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(max_length=100)
    post_desc = models.TextField()
    creation_date = serializers.DateTimeField()
    post_image = serializers.CharField(max_length=255)
    pagination_class = CustomPagination

    #product = ProductSerializer(source='product_set', many=True)

    class Meta:
        model = Post
        fields = ('post_title', 'post_desc', 'creation_date', 'post_image', 'status')#, 'product')
 