from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from openapi_documentor.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path(
        "openapis/",
        include("openapi_documentor.openapi.api.urls", namespace="openapi-api"),
    ),
]
urlpatterns += router.urls
