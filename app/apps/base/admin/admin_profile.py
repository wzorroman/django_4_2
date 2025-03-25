from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.base.models import Profile
from apps.tracking_user.admin import AuditableAdmin
from apps.utils.filters import InputFilter


class UsernameFilter(InputFilter):
    title = "Username"
    parameter_name = "username"

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        elif self.value():
            username = self.value()
            return queryset.filter(user__username=username)


class DocumentNumberFilter(InputFilter):
    title = "Document number"
    parameter_name = "number"

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        elif self.value():
            number = self.value()
            return queryset.filter(document_number=number)


class ProfileAdmin(AuditableAdmin):
    list_display = (
        "id",
        "format_modified",
        "link_username",
        "format_document",
        "full_names",
        "email",
        "celular",
        "whatsapp",
        "format_email",
        "is_active",
    )
    search_fields = ("id", "document_number", "email")
    ordering = ["id"]
    raw_id_fields = ["user", "rol"]
    list_filter = (
        "is_active",
        "user__is_staff",
        "user__is_active",
        "document_type",
        DocumentNumberFilter,
        UsernameFilter,
    )
    readonly_fields = ("created_by", "modified_by", "created", "modified", "full_names")
    date_hierarchy = "created"

    def link_username(self, obj):
        if hasattr(obj, "user") and (obj.user and obj.user.username):
            pre_url = reverse("admin:auth_user_changelist")
            parameters = f"?q={obj.user.username}"
            url = pre_url + parameters
            link = f'<a href="{url}">{obj.user.username}</a>'
            return mark_safe(link)
        return "-"

    def format_document(self, obj):
        cad = "-"
        if obj.document_number:
            cad = f"{obj.get_document_type_display()} {obj.document_number}"
        return cad

    def format_email(self, obj):
        email = ""
        if hasattr(obj, "user") and obj.user:
            email = obj.user.email if obj.user.email else "-"
        return email

    link_username.short_description = "Username"
    link_username.admin_order_field = "user__username"
    format_document.short_description = "Document"
    format_email.short_description = "Email"

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        qs = qs.select_related("rol", "user")
        # qs = qs.prefetch_related("address", "contact")
        return qs


admin.site.register(Profile, ProfileAdmin)
