import pytest
from django.conf import settings
from openapi_documentor.users.models import User
from openapi_documentor.users.tests.factories import UserFactory
from openapi_documentor.openapi.tests.factories import DocumentFactory


open_api_file = settings.APPS_DIR / "openapi/tests/fixtures/hello.yaml"
with open(open_api_file) as fout:
    open_api_doc = fout.read()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def document(openapi) -> User:
    return DocumentFactory(doc=openapi)


@pytest.fixture
def openapi() -> str:
    return open_api_doc
