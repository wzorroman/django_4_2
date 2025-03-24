from __future__ import unicode_literals

from django.contrib import admin

from apps.tracking_user.models import AuditableModel


# from apps.tracking_user.models import AuditableModel


class AuditableAdmin(admin.ModelAdmin):
    exclude = (
        "created_by",
        "modified_by",
    )
    readonly_fields = ("created_by", "modified_by", "created", "modified")

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.created_by = request.user
    #     obj.modified_by = request.user
    #     obj.save()

    def save_formset(self, request, form, formset, change):
        form_super = super().save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        for instance in instances:
            # Check if it is the correct type of inline
            if not isinstance(instance, AuditableModel):
                continue
            if not instance.created_by:
                instance.created_by = f"{request.user.id} {request.user.username}"
            instance.modified_by = f"{request.user.id} {request.user.username}"
            instance.save()
        return form_super

    def format_created(self, obj):
        return obj.created.strftime("%d/%m/%Y %H:%M:%S") if obj.created else "-"

    def format_modified(self, obj):
        return obj.modified.strftime("%d/%m/%Y %H:%M:%S") if obj.modified else "-"

    format_created.short_description = "Created"
    format_created.admin_order_field = "created"
    format_modified.short_description = "Modified"
    format_modified.admin_order_field = "modified"


class StatusAuditableAdmin(admin.ModelAdmin):
    exclude = ("termination_by",)
    readonly_fields = ("termination", "termination_by")
    list_display = ("format_termination", "termination_by", "is_active")
    list_filter = ("is_active", "is_cancelled")

    def format_termination(self, obj):
        return obj.termination.strftime("%d/%m/%Y %H:%M:%S") if obj.termination else "-"

    format_termination.short_description = "Termination"
    format_termination.admin_order_field = "termination"
