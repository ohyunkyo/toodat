from datetime import datetime

from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Q, F

from rest_framework.response import Response
from rest_framework import status

from apps.product.models import Product
from apps.coupon.models import Coupon


def index(request):
    # 쿠폰 임의로 지정
    coupon_id = 1
    try:
        coupon = Coupon.objects.get(pk=coupon_id)
    except Coupon.DoesNotExist:
        return Response(data={"detail": "존재하지 않는 쿠폰입니다!"}, status=status.HTTP_404_NOT_FOUND)

    # 이벤트 기간
    start_dt = datetime(2023, 1, 1)  # Year, Month, Day, Hour, Minute, Second
    end_dt = datetime(2023, 12, 31, 23, 59, 59)  # Year, Month, Day, Hour, Minute, Second

    # 현재 시간
    current_dt = datetime.now()

    if start_dt < current_dt < end_dt:
        is_expired = False
    else:
        is_expired = True

    # 잔여 수량 annotate
    products = Product.objects.all().annotate(
        coupon_redeemed=Count("couponauthority"), filter=(Q(couponauthority__coupon=coupon))
    ).annotate(
        coupon_remain=F("couponauthority__coupon__count_limit") - F("coupon_redeemed")
    )

    template = loader.get_template('promotion/index.html')
    context = {
        'is_expired': is_expired, 'products': products, 'coupon_id': coupon_id
    }
    return HttpResponse(template.render(context, request))
