from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from .models import Truck , Product
from .utils import checkAvailability
# Create your views here


def error_404_view(request,exception):
    data = {"name": "ThePythonDjango.com"}
    return Response(data)


@api_view(['POST'])
def BuyProductView(request):
	try:
		product = request.data.get('product',None)
		truck = request.data.get('truck',None)
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
		if regex.search(product) != None or regex.search(truck) != None:
			return Response({'message': 'Invalid data'},status.HTTP_406_NOT_ACCEPTABLE)
		if product is not None or truck is not None:
			if len(product) > 20 or len(truck) > 20:
				return Response({'message': 'Invalid data'},status.HTTP_406_NOT_ACCEPTABLE)
			truck_qs = Truck.objects.filter(slug=truck)
			if truck_qs.exists() and product:
				truck = truck_qs.first()
				product_qs = Product.objects.filter(truck=truck,slug=product)
				if product_qs.exists():
					product = product_qs.first()
					available = checkAvailability(product.id)
					if available:
						product.quantity -= 1
						product.save()
						truck.money_made += product.price
						truck.save()
						return Response({"message":"ENJOY !"})
					else:
						return Response({"message":"SORRY !"},status=status.HTTP_404_NOT_FOUND)
				else:
					return Response({"message":"Invalid Product ID"},status=status.HTTP_404_NOT_FOUND)
			else:
				return Response({'message':'Wrong Truck , Please try again.'},status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({'message':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def TotalSalesView(request,truck):
	truck_qs = Truck.objects.filter(slug=truck)
	if truck_qs.exists():
		truck = truck_qs.first()
		return Response({'truck':truck.name,'total_sales':truck.money_made})
	else:
		return Response({'message':'Invalid Truck identified'},status=status.HTTP_404_NOT_FOUND)
