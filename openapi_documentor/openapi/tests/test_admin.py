from unittest.mock import Mock

import pytest
from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from openapi_documentor.openapi.models import Document
from openapi_documentor.openapi.admin import DocumentAdmin
from openapi_documentor.openapi.tests.factories import DocumentFactory
from openapi_documentor.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestDocumentAdmin:
    def test_add(self, admin_client, user, openapi):
        url = reverse("admin:openapi_document_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "title": "MyApiDoc",
                "doc": openapi,
                "owner": user.pk,
                "version": "3.0.0",
                "rev": "1.0.0",
                "tags": ["test"],
            },
        )
        assert response.status_code == 302
        assert Document.objects.filter(title="MyApiDoc", owner=user).exists()

    def test_list_docs_with_editor_access(self):
        user1 = UserFactory()
        user2 = UserFactory()
        u1_private_doc = DocumentFactory.create_batch(3, owner=user1)
        u1_shared = DocumentFactory.create_batch(2, owner=user1)
        # user1 shared editor access with user2
        for d in u1_shared:
            d.editors.add(user2)

        u2_private_doc = DocumentFactory.create_batch(2, owner=user2)

        doc_admin = DocumentAdmin(model=Document, admin_site=AdminSite())
        qs1 = doc_admin.get_queryset(request=Mock(user=user1))

        assert qs1.count() == len(u1_private_doc + u1_shared)

        qs2 = doc_admin.get_queryset(request=Mock(user=user2))
        assert qs2.count() == len(u2_private_doc + u1_shared)
