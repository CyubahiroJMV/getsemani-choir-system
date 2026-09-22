from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# INZIRA NKURU Z'UMUSHINGA (TWAZIKOSOYE NGO ZIYOBOKE CHOIR_APP ZIKUREHO NOT FOUND)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('choir_app.urls')), # Iyi ihatira Django kujya kusoma uburinzi muli choir_app direkti
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
