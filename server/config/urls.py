from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.static import static

api_v1 = 'api/v1'

urlpatterns = [
    path(f'{api_v1}/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    # django будет отдавать статические файлы даже в продакшен среде, необходимо для корректной работы админки
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
