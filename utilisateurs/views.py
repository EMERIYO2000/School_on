from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

import requests
from drf_spectacular.utils import extend_schema
from django.utils.crypto import get_random_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from utilisateurs.serializers import ClassicRegisterUserSerializer, GoogleAuthSerializer, LoginSerializer

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def get_tokens_for_user(self, user):
        """Génère manuellement les tokens JWT pour l'utilisateur"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    @extend_schema(
        request=ClassicRegisterUserSerializer,
        responses={
            201: {"message": "Compte créé avec succès !",
                   "user": {"id": "int", "email": "string", "full_name  ": "string", "username": "string"},
                   "tokens": {"refresh": "string", "access": "string"}},
            400: {"error": "Détails de l'erreur de validation"}
        })
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """Endpoint : /api/auth/register/"""
        serialiser = ClassicRegisterUserSerializer(data=request.data)
        if serialiser.is_valid():
            user = serialiser.save()
            tokens = self.get_tokens_for_user(user)
            return Response({
                "message": "Compte créé avec succès !",
                "user": {"id": user.id, "email": user.email, "full_name": user.get_full_name(), "username": user.username},
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
        request=GoogleAuthSerializer,
        responses={
            200: {"message": "Connexion réussie via Google !",
                   "user": {"id": "int", "email": "string", "full_name": "string", "username": "string", "is_teacher": "boolean"},
                   "tokens": {"refresh": "string", "access": "string"}},
            400: {"error": "Détails de l'erreur"}
        }
    )
    @action(detail=False, methods=['post'], url_path='google')
    def register_or_login_google(self, request):
        """Endpoint : /api/auth/google/"""
        serializer = GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['id_token']
        
        if not token:
            return Response({"error": "Le champ id_token est requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 1. Validation du token auprès de Google
            # Remplacer 'VOTRE_GOOGLE_CLIENT_ID' par ton identifiant client Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), 'VOTRE_GOOGLE_CLIENT_ID')
            
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
        except ValueError:
            return Response({"error": "Token Google invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Logique de création ou de connexion
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': first_name,
                'last_name': last_name,
                # On génère un mot de passe aléatoire inutilisable puisque l'accès se fait via Google
                'password': get_random_string(40) 
            }
        )
        
        # 3. Réponse avec les accès
        tokens = self.get_tokens_for_user(user)
        message = "Inscription réussie via Google !" if created else "Connexion réussie via Google !"
        
        return Response({
            "message": message,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.get_full_name(),
                "username": user.username,
                "is_teacher": user.is_teacher
            },
            "tokens": tokens
        }, status=status.HTTP_200_OK)
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {"message": "Connexion réussie !",
                   "user": {"id": "int", "email": "string", "full_name": "string", "username": "string", "is_teacher": "boolean"},
                   "tokens": {"refresh": "string", "access": "string"}},
            400: {"error": "Détails de l'erreur"}
        }
    )
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """Endpoint : /api/auth/login/"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        login_id = serializer.validated_data['login_id']
        password = serializer.validated_data['password']
        
        # C'est ici que la magie de notre backend personnalisé opère !
        # Django va chercher 'login_id' dans le champ email ET dans le champ username.
        user = authenticate(request, username=login_id, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response({"error": "Ce compte est désactivé."}, status=status.HTTP_403_FORBIDDEN)
                
            # Génération des tokens JWT pour la session de l'utilisateur
            tokens = self.get_tokens_for_user(user)
            
            return Response({
                "message": "Connexion réussie !",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.get_full_name(),
                    "username": user.username,
                    "is_teacher": user.is_teacher  # Permet au frontend de savoir s'il faut afficher l'espace mentor
                },
                "tokens": tokens
            }, status=status.HTTP_200_OK)
            
        # Sécurité : On reste vague sur l'erreur pour éviter de donner des indices aux hackers
        return Response(
            {"error": "Identifiants invalides. Veuillez réessayer."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )













# ==========================================
# 1. INSCRIPTION CLASSIQUE (FORMULAIRE MANUEL)
# ==========================================
# class ClassicRegisterUserView(APIView):
#     # Tous le monde doit pouvoiraccéder à ce point pour s'inscrire
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         serializer = ClassicRegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message":"Utilisateur créé avec succès !"},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# # ==========================================
# # 2. INSCRIPTION / CONNEXION VIA GOOGLE
# # ==========================================
# class GoogleLoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = GoogleAuthSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         token = serializer.validated_data['id_token']
        
#         if not token:
#             return Response({"error":"Le champ id_token est requis"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             # validation du token auprès de Google
#             idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            
#             email = idinfo.get('email')
#             first_name= idinfo.get('given_name', '')
#             last_name= idinfo.get('family_name', '')
            
#             if not email:
#                 return Response({"error":"Impossible de récupérer l'email depuis Google."}, status=status.HTTP_400_BAD_REQUEST) 
            
#             # création ou récupération de l'utilisateur
#             username = email.split('@')[0]
#             user, created = User.objects.get_or_create(
#                 email=email,
#                 defaults={
#                     'username':username,
#                     'first_name':first_name,
#                     'last_name':last_name,
#                     'is_teacher': False
#                 }
#             )
#             # Génération des jetons JWT SCHOOL ON
#             refresh = RefreshToken.for_user(user)
            
#             return Response({
#                 "message":"Connexion réussi avec Google !",
#                 "is_new_user": created,
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#             }, status=status.HTTP_200_OK)
            
#         except ValueError:
#             return Response({"error":"Le token Google est invalide ou expiré."}, status=status.HTTP_4)