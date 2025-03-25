import uuid
from datetime import datetime

# audit
from crum import get_current_user
from django.db import models


class AuditableModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField("Created by", max_length=50)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.CharField("Modified by", max_length=50)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk and hasattr(user, "username"):
            self.created_by = f"{user.username}"
        if hasattr(user, "username"):
            self.modified_by = f"{user.username}"
        super().save(force_insert, force_update, using, update_fields)


class StatusAuditableModel(models.Model):
    termination = models.DateTimeField("Termination date", null=True, blank=True)
    termination_by = models.CharField(
        "Termination by", max_length=50, null=True, blank=True
    )
    is_active = models.BooleanField("Is active?", default=True)
    is_cancelled = models.BooleanField("Is cancelled?", default=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        # if self.is_cancelled:
        #     raise ValueError("El registro esta anulado")
        if not self.is_active and user:
            self.termination = datetime.now()
            self.termination_by = f"{user.username}"
        super().save(force_insert, force_update, using, update_fields)


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True