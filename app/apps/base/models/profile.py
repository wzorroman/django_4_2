from django.contrib.auth.models import User
from django.db import models

from apps.commons.constants import DOCUMENT_TYPE_CHOICES, DOCUMENT_TYPE_UNKNOWN, ROL_ID_CLIENTE
from apps.tracking_user.models import AuditableModel


class Rol(models.Model):
    description = models.CharField("Description", max_length=50,
                                   help_text="ejem: Clientes, profesionales, administradores")
    is_active = models.BooleanField("Is active", default=True)

    def __str__(self):
        return f"{self.description}"

    class Meta:
        verbose_name_plural = "Usuarios Roles"
        permissions = (
            ("access_rol", "rol access"),
            ("list_rol", "rol list"),
            ("module_mantenimiento", "** modulo mantenimiento"),
            ("module_usuarios", "** modulo usuarios"),
        )

    @staticmethod
    def get_combo_roles_actives():
        list_rol = Rol.objects.filter(is_active=True)
        combo = [("", "- Seleccione -")]
        for item in list_rol:
            combo.append((item.pk, item.description))
        return combo


class Profile(AuditableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    rol = models.ForeignKey(Rol, verbose_name="Rol", related_name="profiles", on_delete=models.DO_NOTHING,
                            blank=True, null=True,)
    document_type = models.CharField(
        "Document type",
        max_length=15,
        blank=True,
        null=True,
        choices=DOCUMENT_TYPE_CHOICES,
        default=DOCUMENT_TYPE_UNKNOWN,
    )
    document_number = models.CharField(
        "Document number", max_length=15, db_index=True, null=True, blank=True
    )
    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50, db_index=True)
    second_last_name = models.CharField(
        "Second lastName", max_length=50, null=True, blank=True
    )
    full_names = models.CharField(
        "Complete name", max_length=250, null=True, blank=True
    )
    email = models.EmailField("email", null=True, blank=True)
    celular = models.CharField("Celular", max_length=15, null=True, blank=True)
    whatsapp = models.CharField("whatsapp", max_length=15, null=True, blank=True)
    is_active = models.BooleanField("Is active", default=True)
    observations = models.TextField("Observations", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Usuarios perfiles"
        unique_together = ("document_type", "document_number")

    def __str__(self):
        name = f"{self.full_names}" if self.full_names else ""
        try:
            email = f" - ({self.user.email})" if self.user.email else ""
        except Exception as e:
            email = ""
        return f"({self.pk}) | {name}{email}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        full_surnames = ""
        if self.last_name:
            full_surnames = f"{self.last_name}"
        if self.second_last_name:
            full_surnames = f"{full_surnames} {self.second_last_name}"
        if full_surnames and full_surnames.strip() != "":
            full_surnames = full_surnames.strip().upper()

        nombres = self.first_name.strip().upper() if self.first_name else None
        if nombres and full_surnames:
            self.full_names = f"{nombres} {full_surnames}"

        if hasattr(self, "user") and self.user:
            if not self.user.is_superuser:
                self.user.is_active = self.is_active
            if nombres:
                self.user.first_name = self.first_name.upper()
            if full_surnames:
                self.user.last_name = full_surnames
            self.user.email = self.email
            self.user.save()
        else:
            user = User()
            user.first_name = self.first_name
            user.last_name = full_surnames
            user.is_active = True
            user.username = self.document_number
            user.email = self.email
            user.save()

        super().save(force_insert, force_update, using, update_fields)

    @property
    def get_full_surnames(self):
        full_surnames = None
        if self.last_name:
            full_surnames = f"{self.last_name}"
        if self.second_last_name:
            full_surnames = f"{full_surnames} {self.second_last_name}"

        if full_surnames and full_surnames.strip() != "":
            full_surnames = full_surnames.strip().upper()
        return full_surnames
