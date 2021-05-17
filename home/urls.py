from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home , name='FERS-home'),
    path('live/', views.livefe , name='FERS-live-feed'),
    path('image/predict/', views.predict , name='predict'),
    path('image/', views.image_part, name='image'),
    path('report/', views.reportBug, name='report')
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)