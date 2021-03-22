from django.contrib import admin

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
        return qs.filter(owner=request.user)
