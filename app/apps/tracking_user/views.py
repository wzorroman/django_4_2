from django.shortcuts import render  # noqa


class AuditableMixin(object,):
    def form_valid(self, form):
        if not form.instance.id:
            form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
