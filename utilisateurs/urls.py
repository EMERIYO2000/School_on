from django.urls import include, path
from rest_framework.routers import DefaultRouter
from utilisateurs.views import AuthViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),               
]