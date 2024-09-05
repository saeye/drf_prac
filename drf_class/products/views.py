from django.core.cache import cache
from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.decorators import api_view

from .serializers import ProductSerializer
from .models import Products


@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"

    if not cache.get(cache_key):
        print("cache miss")
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_response = serializer.data
        cache.set("product_list", json_response)
    
    response_data = cache.get(cache_key)
    return Response(response_data)
