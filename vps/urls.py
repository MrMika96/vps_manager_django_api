from django.urls import path

from vps import views

urlpatterns = [
    path("", views.VpsViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("<uuid:pk>", views.VpsViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),
    path("status_update/<uuid:pk>", views.VpsStatusUpdateView.as_view())
]