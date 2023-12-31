from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('account/',include('user.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('comment/', include('comment.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
