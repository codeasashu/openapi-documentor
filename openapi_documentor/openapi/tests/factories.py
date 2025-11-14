from factory import Faker
from factory.django import DjangoModelFactory
from openapi_documentor.openapi.models import Document


class DocumentFactory(DjangoModelFactory):
    title = Faker("user_name")

    class Meta:
        model = Document
