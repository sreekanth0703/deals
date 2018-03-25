from rest_framework import serializers
from deals.models import *

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
    #product = ProductSerializer(source='product_set', many=True)

    class Meta:
        model = Post
        fields = ('post_title', 'post_desc', 'creation_date', 'status')#, 'product')
