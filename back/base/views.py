import django
from django.http import HttpRequest, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from base.models import UserAssignment
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



@csrf_exempt
def handleRequest(request):
    # Manually authenticate using JWT
    auth = JWTAuthentication()
    try:
        # Extract and authenticate the token
        user, _ = auth.authenticate(request)
    except AuthenticationFailed:
        return HttpResponse("Authentication failed", status=401)

    # Get the user's assignments
    user_assignments = UserAssignment.objects.filter(user=user)

    # Format the assignments into a list of assignment IDs or any other data you prefer
    assignments_list = user_assignments  # Or use any other field you prefer

    # Prepare user info to be sent as headers
    headers = {
        'X-User-Username': user.username,
        'X-User-Email': user.email,
        'X-User-Admin': str(user.is_superuser),  # Convert boolean to string
        'X-User-Assignments': ','.join(map(str, assignments_list)),  # Join assignment IDs into a comma-separated string
    }

    # Return user info in the headers of the response
    return HttpResponse(f"Authenticated user: {str(user)}", headers=headers)