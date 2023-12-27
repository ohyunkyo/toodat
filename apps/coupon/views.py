from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.coupon.models import Coupon, CouponAuthority


class CouponAuthorityAPI(APIView):
	def post(self, request, *args, **kwargs):
		# 쿠폰 가져오기
		coupon_id = request.data.get('coupon_id')
		try:
			coupon = Coupon.objects.get(pk=coupon_id)
		except Coupon.DoesNotExist:
			return Response(data={"detail": "존재하지 않는 쿠폰입니다!"}, status=status.HTTP_404_NOT_FOUND)

		# 제품 가져오기
		product_id = request.data.get('product_id')

		# 쿠폰-제품 으로 발급된 쿠폰함 목록
		coupon_authorities = CouponAuthority.objects.filter(coupon=coupon, product_id=product_id)

		# 사용자 정보를 임의로 지정
		user_id = request.data.get('user_id')
		user = get_object_or_404((get_user_model()), pk=user_id)
		# todo: 인증된 사용자의 정보를 대신 사용하도록 수정

		# 해당 사용자가 쿠폰을 발급 받은적 있는지
		user_coupon_authorities = coupon_authorities.filter(user=user)

		if user_coupon_authorities:
			return Response(data={"detail": "이미 발급 받은 쿠폰입니다!"}, status=status.HTTP_409_CONFLICT)
		else:

			if 0 < coupon.count_limit <= coupon_authorities.count():
				return Response(data={"detail": "발급 수량을 초과하여 발급 불가능합니다!"}, status=status.HTTP_409_CONFLICT)
			else:
				CouponAuthority.objects.create(user=user, coupon=coupon, product_id=product_id)

		return Response(data={"detail": "쿠폰 발급이 완료되었습니다!"})
