import json
import uuid

import yaml

try:
    from yaml import Loader as YamlLoader
except ImportError:
    from yaml import YamlLoader

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from openapi_spec_validator import validate_spec
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from openapi_documentor.users.models import User


class TaggedDocument(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class OpenapiVersions(models.TextChoices):
    THREEZERO = "3.0.0", "3.0.0"
    THREEONE = "3.0.1", "3.0.1"
    THREETWO = "3.0.2", "3.0.2"


class Document(models.Model):
    """Each revision represents a oas document"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, default="Openapi doc")
    doc = models.TextField(blank=True)  # Text field
    rev = models.CharField(max_length=20, default="1.0.0")  # revision (v1.0)
    formatted = models.TextField(blank=True, null=True, editable=False)
    version = models.CharField(
        choices=OpenapiVersions.choices,
        max_length=20,
        default=OpenapiVersions.THREEZERO,
    )  # oas 3.0
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    created = models.DateTimeField("date published", auto_now_add=True)
    modified = models.DateTimeField("date modified", auto_now=True)
    editors = models.ManyToManyField(User, default=None, related_name="editors", blank=True)
    tags = TaggableManager(through=TaggedDocument)

    class Meta:
        ordering = ["-modified"]

    def clean(self):
        parsed_doc = self._parse_doc(self.doc)
        if not parsed_doc:
            raise ValidationError(_("Only Json and Yaml are allowed"))
        try:
            validate_spec(parsed_doc)
        except:  # noqa: E722
            raise ValidationError({"doc": _("Not a valid openapi schema")})

    def save(self, *args, **kwargs):
        parsed_doc = self._parse_doc(self.doc)
        if parsed_doc:
            self.formatted = json.dumps(parsed_doc)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("openapis:detail", args=[str(self.id)])

    def _parse_doc(self, doc):
        spec = None
        try:
            spec = json.loads(doc)
        except json.JSONDecodeError:
            try:
                spec = yaml.load(doc, Loader=YamlLoader)
            except yaml.YAMLError:
                return None
        return spec
