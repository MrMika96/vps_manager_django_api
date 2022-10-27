from django.urls import path

from applications import views

urlpatterns = [
    path("", views.ApplicationViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("<int:pk>", views.ApplicationViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }))
]
