import json
from datetime import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Document


class OasForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["doc"]
        widgets = {
            "doc": forms.HiddenInput(attrs={"id": "doc_input"}),
        }


def get_version(doc, default="3.0.0"):
    formatted = None
    try:
        formatted = json.loads(doc)
    except json.JSONDecodeError:
        return default
    return formatted.get("openapi", default)


def oas_version(obj):
    version = get_version(obj.formatted)
    return version


oas_version.short_description = "Version"


def front_link(obj):
    return format_html("<a href='/openapis/{}' target='_blank'>View</a>", obj.id)


front_link.short_description = "Link"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    site_header = "Openapi admin"
    save_on_top = True
    submit_buttons_bottom = False
    form = OasForm

    list_display = ("title", oas_version, "owner", front_link)

    add_form_template = "admin/openapi/add.html"
    change_form_template = "admin/openapi/add.html"

    def get_title(self, doc, default="Openapi Document"):
        formatted = None
        try:
            formatted = json.loads(doc)
        except json.JSONDecodeError:
            return default
        info = formatted.get("info", {"title": default})
        return info["title"]

    def save_model(self, request, obj, form, change):
        obj.title = self.get_title(obj.formatted)
        obj.owner_id = request.user.id
        obj.created = datetime.now()
        obj.modified = datetime.now()
        super().save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["spec_id"] = object_id
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )
