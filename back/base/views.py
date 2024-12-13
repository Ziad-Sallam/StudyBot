from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Check if the user is a superuser (administrator)
            is_admin = user.is_superuser
            
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'is_admin': is_admin,  # Add the is_admin field to the response
            })
        
        return Response({'error': 'Invalid credentials'}, status=400)
