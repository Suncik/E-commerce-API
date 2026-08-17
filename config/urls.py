from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.catalog.urls")),
    path("api/v1/", include("apps.cart.urls")),
     path("api/v1/", include("apps.orders.urls")),
     path("api/v1/", include("apps.users.urls")),
    
]