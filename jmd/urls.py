from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

admin.site.site_header = "JMD Promotions Admin"
admin.site.site_title  = "JMD Admin"
admin.site.index_title = "Welcome to JMD Promotions Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('shop/', include('store.urls')),
    # Serve media files in both DEBUG and production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
