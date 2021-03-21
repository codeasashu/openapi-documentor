from django.urls import path

from openapi_documentor.openapi.views import (
    api_list_view,
    api_detail_view,
    api_tagged_view
)

app_name = "openapi"
urlpatterns = [
    path("", view=api_list_view, name="list"),
    path("tagged/<str:tag>", view=api_tagged_view, name="tag"),
    path("<slug:pk>/", view=api_detail_view, name="detail"),
]
