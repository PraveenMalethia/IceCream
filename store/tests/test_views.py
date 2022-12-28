from django.urls import reverse
from rest_framework.test import APIClient , APITestCase
from rest_framework import status
from store.models import Truck , Product 
import json

# Create your tests here.

class StoreViewsTests(APITestCase):

	def setUp(self):
		self.truck = Truck.objects.create(name='test-truck',slug='test-truck')
		self.product = Product.objects.create(
			truck=self.truck,
			name='test-ice-cream',
			slug='test-ice-cream',
			price=10,
			flavour='Chocolate',
			quantity=2,
		)
		self.assertEqual(Truck.objects.count(), 1)
		self.assertEqual(Product.objects.count(), 1)

	def money_made_zero_test(self):
		self.assertEqual(self.truck.money_made == 0,True)

	def test_buy_ice_cream(self):
		self.client = APIClient()
		payload = {
			'product':self.product.slug,
			'truck':self.truck.slug
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# variables for previous values
		prev_quantity = self.product.quantity
		prev_account_total = self.truck.money_made
		# updating class data with latest instance data
		self.truck = Truck.objects.get(id=self.truck.id)
		self.product = Product.objects.get(id=self.product.id)
		# actual tests
		self.assertEqual(self.product.quantity, prev_quantity-1)
		self.assertEqual(self.truck.money_made,prev_account_total+self.product.price)
		self.assertEqual(self.truck.money_made > 0,True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response_body.get('message'), 'ENJOY !')
	
	def test_buy_but_no_products_available(self):
		self.client = APIClient()
		# Let's purchase all available ice cream
		# quantity is only 2 so we will call twice this function.
		self.test_buy_ice_cream()
		self.test_buy_ice_cream()
		payload = {
			'product':self.product.slug,
			'truck':self.truck.slug
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# updating class data with latest instance data
		self.truck = Truck.objects.get(id=self.truck.id)
		self.product = Product.objects.get(id=self.product.id)
		# actual tests
		self.assertEqual(self.truck.money_made > 0,True)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response_body.get('message'), 'SORRY !')
	
	def test_buy_ice_cream_no_truck_found(self):
		self.client = APIClient()
		payload = {
			'product':self.product.slug,
			'truck':'non-existing-slug'
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response_body.get('message'), 'Wrong Truck , Please try again.')
	
	def test_buy_ice_cream_long_truck_slug(self):
		self.client = APIClient()
		payload = {
			'product':self.product.slug,
			'truck':'non-existing-very-long-slug'
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
		self.assertEqual(response_body.get('message'), 'Invalid data')
	
	def test_buy_ice_cream_no_icecream_found(self):
		self.client = APIClient()
		payload = {
			'product':'non-existing-very-long-product-slug',
			'truck':self.truck.slug
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
		self.assertEqual(response_body.get('message'), 'Invalid data')
	
	def test_buy_ice_cream_no_icecream_found(self):
		self.client = APIClient()
		payload = {
			'product':'invalid-product',
			'truck':self.truck.slug
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(response_body.get('message'), 'Invalid Product ID')
	
	def test_buy_ice_cream_special_characters(self):
		self.client = APIClient()
		payload = {
			'product':'##',
			'truck':'$$'
		}
		url = reverse('store:buy-product')
		response = self.client.post(url, payload, format='json')
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
		self.assertEqual(response_body.get('message'), 'Invalid data')
	
	def test_buy_ice_cream_invalid_payload(self):
		self.client = APIClient()
		url = reverse('store:buy-product')
		# we are not sending any payload to the endpoint
		response = self.client.post(url)
		response_body = json.loads(response.content.decode('UTF-8'))
		# actual tests
		self.money_made_zero_test()
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_check_total_sales(self):
		self.test_buy_ice_cream()
		# check total sales after buying
		url = reverse('store:check-total-sales',args=[self.truck.slug])
		response = self.client.get(url)
		response_body = json.loads(response.content.decode('UTF-8'))
		self.assertEqual(response_body.get('truck'), self.truck.slug)
		self.assertEqual(response_body.get('total_sales'), self.truck.money_made)
		self.assertEqual(response_body.get('total_sales') > 0, True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)