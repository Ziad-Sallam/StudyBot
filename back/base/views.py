import stat
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
from django.contrib.auth.models import User

from base.models import Assignment, AssignmentStatus, AssignmentType, Materials, Subject, UserAssignment
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
def createAssignment(request: HttpRequest):
    deadline = request.GET.get('deadline')
    subject = request.GET.get('subject')
    assignment_type = request.GET.get('type')  # Get the assignment type from the request

    subjectObject = Subject.objects.get(name=subject)
    assignmentTypeObject = AssignmentType.objects.get(type=assignment_type)
    pendingStatus = AssignmentStatus.objects.get(id=2)  # Assuming id 2 is for "Pending" status

    auth = JWTAuthentication()
    try:
        user, _ = auth.authenticate(request)
        if user.is_superuser:
            assignment = Assignment.objects.create(subject=subjectObject, type=assignmentTypeObject, deadline=deadline)
            
            # Create a UserAssignment for each user with the new assignment and pending status
            users = User.objects.all()
            for user in users:
                UserAssignment.objects.create(user=user, assignment=assignment, status=pendingStatus)
            
            return HttpResponse(assignment)
    except AuthenticationFailed:
        return HttpResponse("Authentication failed", status=401)

def getMaterial(request : HttpRequest):
    subject = request.GET.get('subject')
    materials = Materials.objects.filter(subject__name=subject)
    return HttpResponse(materials)

def addMaterial(request : HttpRequest):
    subject = request.GET.get('subject')
    file = request.FILES['file']
    subjectObject = Subject.objects.get(name=subject)
    material = Materials.objects.create(subject=subjectObject, file=file)
    return HttpResponse(material, status=201)
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