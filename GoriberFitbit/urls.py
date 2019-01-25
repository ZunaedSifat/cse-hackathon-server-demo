from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from GoriberFitbit.api import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)

urlpatterns = [
    # Authentication token
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Signup and confirmation
    path('signup/', views.Signup.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.Activate.as_view(), name='activate'),

    path('', views.Home.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('data/session/', views.SessionData.as_view(), name='session_data'),
    path('data/heart/', views.HeartData.as_view(), name='bpm_data'),
    path('leaderboard/', views.LeaderBoardView.as_view(), name='leaderboard'),

    path('admin/', admin.site.urls),
    path('models/', include(router.urls)),
]
