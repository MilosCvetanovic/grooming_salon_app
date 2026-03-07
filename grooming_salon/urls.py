"""
URL configuration for grooming_salon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from grooming_salon import settings

#-----------------------------------------------------------------------------------------------------------------------
handler404 = 'grooming_salon.common.views.error_404'
handler500 = 'grooming_salon.common.views.error_500'

#-----------------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grooming_salon.common.urls')),
    path('accounts/', include('grooming_salon.accounts.urls')),
    path('dogs/', include('grooming_salon.dogs.urls')),
    path('services/', include('grooming_salon.services.urls')),
]

#-----------------------------------------------------------------------------------------------------------------------
# Neophodno za rad sa medijskim datotekama
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#-----------------------------------------------------------------------------------------------------------------------
# Ovaj blok forsira Django da služi medijske datoteke čak i kada je DEBUG=False
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

#-----------------------------------------------------------------------------------------------------------------------
