"""
URL configuration for fuelapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from schema_graph.views import Schema

urlpatterns = [
    # polite-elephant is my admin address (from default admin/)
    path("polite-elephant/", admin.site.urls),
    path('polite-elephant/defender/', include('defender.urls')),
    path('', include('orders.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    path("schema/", Schema.as_view()),
]
