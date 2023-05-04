from django.urls import path
from rest_framework_nested import routers
from .views import ChangePasswordViewSet, CreateUserViewset, CustomTokenObtainPairView

router = routers.SimpleRouter()
router.register('users', CreateUserViewset, basename='users')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('change_password/<int:pk>/',
         ChangePasswordViewSet.as_view({'put': 'update'}), name='auth_change_password'),
]


urlpatterns += router.urls
