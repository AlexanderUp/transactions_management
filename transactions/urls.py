from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, ItemViewSet, TransactionViewSet

v1_router = DefaultRouter()
v1_router.register("items", ItemViewSet)
v1_router.register("accounts", AccountViewSet, basename="account")
v1_router.register("transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("v1/", include(v1_router.urls)),
]
