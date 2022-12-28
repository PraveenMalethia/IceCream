from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Truck(models.Model):
	"""
	Truck Table to store different ice cream trucks with their name

	Name will distinguish which truck is this , if they open multiple franchise
	"""
	name = models.CharField(max_length=20)
	slug = models.SlugField(null=False, unique=True)
	money_made = models.BigIntegerField(default=0)

	def __str__(self):
		return self.name



class Product(models.Model):
	
	"""
	Product Table to store product information with respect to their owner
	"""
	# Product Flavours constant

	# However we can make a different model just for flavours
	FLAVOURS = (
		('Chocolate','Chocolate'),
		('Pistachio','Pistachio'),
		('Strawberry','Strawberry'),
		('Mint','Mint'),
	)
	
	# Product instance fields

	truck = models.ForeignKey(Truck,on_delete=models.CASCADE)
	name = models.CharField(max_length=20)
	slug = models.SlugField(null=False, unique=True)
	price = models.IntegerField()
	flavour = models.CharField(choices=FLAVOURS,max_length=20)
	quantity = models.BigIntegerField(default=1)

	def __str__(self):
		return self.name