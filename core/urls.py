from django.urls import path
from rest_framework_nested import routers
from .views import CreateUserViewset, CustomTokenObtainPairView

router = routers.SimpleRouter()
router.register('users', CreateUserViewset, basename='users')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]

urlpatterns += router.urls
