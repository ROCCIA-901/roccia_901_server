"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("accounts/", include("account.urls")),
        path("attendances/", include("attendance.urls")),
        path("records/", include("record.urls")),
        path("rankings/", include("ranking.urls")),
        path("mypages/", include("mypage.urls")),
    ])),
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui",),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc",),
]
