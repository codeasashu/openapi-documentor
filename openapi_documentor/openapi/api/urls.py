from django.urls import path

from .views import OpenapiDetailView, OpenapiListView, OpenapiSpecView

app_name = "openapi-apis"
urlpatterns = [
    path("", view=OpenapiListView.as_view(), name="list"),
    path("<slug:pk>/", view=OpenapiDetailView.as_view(), name="detail"),
    path("<slug:pk>/spec", view=OpenapiSpecView.as_view(), name="spec"),
]
