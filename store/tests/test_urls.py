from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase , APIClient
from store.views import ( TotalSalesView , BuyProductView )

class StoreUrlsTests(APITestCase):

	def setUp(self):
		pass

	def test_buy_url(self):
		url = 'store:buy-product'
		reversed_url = reverse(url)
		resolved = resolve(reversed_url).func
		self.assertEqual(resolved,BuyProductView)

	def test_total_sales_url(self):
		url = 'store:check-total-sales'
		reversed_url = reverse(url,args=['praveen'])
		resolved = resolve(reversed_url).func
		self.assertEqual(resolved,TotalSalesView)