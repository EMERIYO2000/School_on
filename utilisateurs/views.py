from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from utilisateurs.serializers import RegisterUserSerializer

User = get_user_model()

# ==========================================
# 1. INSCRIPTION CLASSIQUE (FORMULAIRE MANUEL)
# ==========================================
class RegisterUserView(APIView):
    # Tous le monde doit pouvoiraccéder à ce point pour s'inscrire
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"Utilisateur créé avec succès !"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# ==========================================
# 2. INSCRIPTION / CONNEXION VIA GOOGLE
# ==========================================
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('id_token')
        
        if not token:
            return Response({"error":"Le champ id_token est requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # validation du token auprès de Google
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            
            email = idinfo.get('email')
            first_name= idinfo.get('given_name', '')
            last_name= idinfo.get('family_name', '')
            
            if not email:
                return Response({"error":"Impossible de récupérer l'email depuis Google."}, status=status.HTTP_400_BAD_REQUEST) 
            
            # création ou récupération de l'utilisateur
            username = email.split('@')[0]
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username':username,
                    'first_name':first_name,
                    'last_name':last_name,
                    'is_teacher': False
                }
            )
            # Génération des jetons JWT SCHOOL ON
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message":"Connexion réussi avec Google !",
                "is_new_user": created,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({"error":"Le token Google est invalide ou expiré."}, status=status.HTTP_4)