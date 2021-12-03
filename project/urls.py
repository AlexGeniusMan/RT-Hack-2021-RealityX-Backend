"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import permissions
from django.contrib import admin
from django.conf import settings
from django.urls import path

import main_app.views as views


urlpatterns = [
    # Main admin panel
    path('admin/', admin.site.urls),

    # Auth
    url(r'^api/auth/', include('djoser.urls')),
    url(r'^api/auth/', include('djoser.urls.jwt')),

    # Return all cameras data
    path('api/get_all_cameras', views.GetAllCamerasView.as_view()),

    # Return camera data
    path('api/get_camera/<int:camera_uid>', views.GetCameraView.as_view()),

    # Update and get cameras data
    path('api/update_cameras', views.UpdateCamerasView.as_view()),

    # Fill database with test data
    path('api/fill_db', views.FillDatabaseView.as_view()),

    # Lol
    path('api/lol', views.Lol.as_view()),
]

# Static and media
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
