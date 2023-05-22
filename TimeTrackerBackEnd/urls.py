"""TimeTrackerBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from TimeTrackerBackEnd import views

API_PREFIX = ''

router = SimpleRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path(API_PREFIX, include(router.urls)),
                  path('login/', views.LoginView.as_view()),
                  path('logout/', views.LogoutView.as_view()),
                  path('profile/', views.ProfileView.as_view()),
                  path('register/', views.UserRegistrationView.as_view()),
                  path('start/', views.StartView.as_view({'post': 'start'})),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
