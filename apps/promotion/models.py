from django.db import models
from django.utils.translation import gettext_lazy as _


class Promotion(models.Model):
    """이벤트 관리용"""

    class Status(models.TextChoices):
        PENDING = "PE", _("Pending")
        ONGOING = "ON", _("Ongoing")
        COMPLETED = "CO", _("Completed")

    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True, help_text="설명 또는 메모")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    start_dt = models.DateTimeField(help_text="이벤트 노출 시작일")
    end_dt = models.DateTimeField(null=True, blank=True, help_text="이벤트 노출 종료일")
