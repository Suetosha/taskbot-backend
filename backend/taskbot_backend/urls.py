from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/categories/", include("apps.categories.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
]
