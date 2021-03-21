from django.urls import path

from openapi_documentor.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_api_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/apis", view=user_api_view, name="apis"),
]
