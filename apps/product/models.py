from django.db import models


class Product(models.Model):
	"""상품"""

	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=1000)
