from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from GoriberFitbit.api import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)

urlpatterns = [
    path('router/', include(router.urls)),
    path('hello/', views.HelloView.as_view(), name='hello'),
    # path('users/', views.UserViewSet, name='groups'),
    # path('groups/', views.GroupViewSet, name='groups'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
