from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utilisateurs.views import RegisterUserView, GoogleLoginView

urlpatterns = [
    # Route pour l'inscription
    path('Register/', RegisterUserView.as_view(), name='auth_register'),
    
    # Route pour la connection (génère le token d'accès et le refresh Token)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Route pour rafraîchir le jeton quand il expire
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 4. Connexion / Inscription via Google
    path('google-login/', GoogleLoginView.as_view(), name='auth_google_login'),
]
