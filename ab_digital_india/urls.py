from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'backend.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('backend.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# customize admin panel
admin.site.site_header = "A. B. DIGITAL INDIA PVT LTD"
admin.site.site_title = "A. B. DIGITAL INDIA PVT LTD"
admin.site.index_title = "Welcome to Admin Area"