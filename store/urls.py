from django.urls import path
from rest_framework.response import Response
from rest_framework import status
from . import views

app_name = 'store'

urlpatterns = [
  path('buy',views.BuyProductView,name="buy-product"),
  path('<str:truck>/total-sales',views.TotalSalesView,name="check-total-sales")
]