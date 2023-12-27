from django.db import models
from django.contrib.auth import get_user_model


class Coupon(models.Model):
    """할인 쿠폰"""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(blank=True, default=0)
    rate = models.PositiveIntegerField(blank=True, default=0)
    expire_at = models.DateTimeField(blank=True, null=True, default=None, help_text="해당 쿠폰을 언제까지 redeem 가능한지")
    count_limit = models.PositiveIntegerField(default=0)


class CouponAuthority(models.Model):
    """할인 쿠폰함"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coupon = models.ForeignKey("coupon.Coupon", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
