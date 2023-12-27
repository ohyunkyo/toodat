import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from apps.product.models import Product
from apps.coupon.models import Coupon

client = Client()


class CouponAuthorityTest(TestCase):
	def setUp(self):
		self.coupon = Coupon.objects.create(
			name="테스트 무료쿠폰",
			code="TEST01",
			value=0,
			rate=100,
			count_limit=2
		)

		self.product = Product.objects.create(
			name="테스트 작품",
			description="테스트중입니다"
		)

		self.user_01 = get_user_model().objects.create(
			username="testuer01",
			password="testpass11@@"
		)

	def tearDown(self):
		self.coupon.delete()
		self.product.delete()

	def test_create_coupon_authority(self):
		data = {
			'coupon_id': self.coupon.pk,
			'product_id': self.product.pk,
			'user_id': self.user_01.pk
		}
		response = client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {
			"detail": "쿠폰 발급이 완료되었습니다!"
		})

	def test_duplicate_coupon_authority(self):
		data = {
			'coupon_id': self.coupon.pk,
			'product_id': self.product.pk,
			'user_id': self.user_01.pk
		}
		client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')
		response = client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 409)
		self.assertEqual(response.json(), {
			"detail": "이미 발급 받은 쿠폰입니다!"
		})

	def test_limit_coupon_authority(self):
		user_02 = get_user_model().objects.create(
			username="testuer02",
			password="testpass11@@"
		)

		user_03 = get_user_model().objects.create(
			username="testuer03",
			password="testpass11@@"
		)

		data = {
			'coupon_id': self.coupon.pk,
			'product_id': self.product.pk,
			'user_id': self.user_01.pk
		}
		client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')

		data['user_id'] = user_02.pk
		client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')

		data['user_id'] = user_03.pk
		response = client.post('/api/coupon_authority/', json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 409)
		self.assertEqual(response.json(), {
			"detail": "발급 수량을 초과하여 발급 불가능합니다!"
		})
