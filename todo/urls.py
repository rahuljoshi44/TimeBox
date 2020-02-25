from django.contrib import admin
from django.urls import path, include
# from django.views.generic import TemplateView

# path('', TemplateView.as_view(template_name = "profile.html")),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path('Home', include('register.urls')),
    path('Profile/', include('dash.urls')),
]

