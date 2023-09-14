from django.contrib import admin
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Register your models here.
# from guardian.admin import GuardedModelAdmin
from .models import Document

# admin.site.register(Revision)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"title": ("title",)}
    list_display = ("title", "created")
    search_fields = ("title",)
    ordering = ("-created",)
    date_hierarchy = "created"

    def get_queryset(self, request):
        qs = super(DocumentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(owner=request.user) | Q(editors=request.user)).distinct()

    def change_view(
        self, request: HttpRequest, object_id: str, **kwargs
    ) -> HttpResponse:
        if not (
            request.user.is_superuser
            or request.user.document_set.filter(pk=object_id).exists()
        ):
            self.exclude = ["editors"]
            self.readonly_fields = ["owner"]
        return super().change_view(request, object_id, **kwargs)
