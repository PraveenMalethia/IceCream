from .models import Product

# Helper Function to check Availability of product
def checkAvailability(product_id):
	product = Product.objects.get(id=product_id)
	if product.quantity > 0 :
		return True
	else:
		return False