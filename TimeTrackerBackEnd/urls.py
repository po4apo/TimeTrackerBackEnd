from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt import views as jwt_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from TimeTrackerBackEnd import views

...

schema_view = get_schema_view(
    openapi.Info(
        title="Time Tracker API",
        default_version='v1',
        description="Some description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,
                        ],
)

API_PREFIX = ''

router = SimpleRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [path('admin/', admin.site.urls),

               path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
               path('profile/', views.ProfileView.as_view()),
               path('register/', views.UserRegistrationView.as_view()),

               path(API_PREFIX, include(router.urls)),
               path('start/', views.MangeTimeView.as_view({'post': 'start'})),
               path('stop/', views.MangeTimeView.as_view({'patch': 'stop'})),
               path('status/', views.MangeTimeView.as_view({'get': 'status'})),

               path('time_spent/<int:pk>/', views.StatisticView.as_view({'get': 'task_time_spent'})),

               # re_path(r'^swagger(?P\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
               path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
               path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
               ]


