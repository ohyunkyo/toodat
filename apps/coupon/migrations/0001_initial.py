# Generated by Django 5.0 on 2023-12-27 05:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('value', models.IntegerField(blank=True, default=0)),
                ('rate', models.PositiveIntegerField(blank=True, default=0)),
                ('expire_at', models.DateTimeField(blank=True, default=None, help_text='해당 쿠폰을 언제까지 redeem 가능한지', null=True)),
                ('count_limit', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CouponAuthority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
