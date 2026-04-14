from django.contrib import admin
from django.urls import path
from django.urls import path, include
import users
from users import urls
from .views import landing_page
from users.views import RegisterView, LoginView

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
