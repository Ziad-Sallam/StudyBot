import base64
import json
import django
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from base.models import Assignment, AssignmentStatus, AssignmentType, Materials, Notification, Subject, Tasks, UserAssignment, userNotification
from .SpacyModel import QueryHandler
from .serializers.SubjectSerializer import SubjectSerializer
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
            user.last_login = django.utils.timezone.now()
            # return Response({
            #     'refresh': str(refresh),
            #     'access': str(access_token),
            #     'is_admin': is_admin,  # Add the is_admin field to the response
            # })
            return Response(headers={
                "Authorization" : str(access_token),
                "is_admin" : is_admin
            },data={
                "message": "Login successful"
            }, status=200)   
        
        return Response({'error': 'Invalid credentials'}, status=400)
@csrf_exempt
def createAssignment(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        deadline = data.get('deadline')
        subject = data.get('subject')
        assignment_type = data.get('type')
        description = data.get('description')
        print(description)
        subjectObject = Subject.objects.get(name=subject)
        assignmentTypeObject = AssignmentType.objects.get(type=assignment_type)
        pendingStatus = AssignmentStatus.objects.get(id=2)  # Assuming id 2 is for "Pending" status

        auth = JWTAuthentication()
        try:
            user, _ = auth.authenticate(request)
            if user.is_superuser:
                assignment = Assignment.objects.create(subject=subjectObject, type=assignmentTypeObject, deadline=deadline, description=description)

                # Create a UserAssignment for each user with the new assignment and pending status
                users = User.objects.all()
                for user in users:
                    UserAssignment.objects.create(user=user, assignment=assignment, status=pendingStatus)

                return HttpResponse("Assignment created successfully", status=201)
            else:
                return HttpResponse("You are not authorized to create assignments", status=403)
        except AuthenticationFailed:
            return HttpResponse("Authentication failed", status=401)
@csrf_exempt
def getMaterial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get('subject')

            if not subject:
                return JsonResponse({"error": "Subject is required"}, status=400)

            # Get the subject object
            subjectObject = Subject.objects.get(name=subject)

            # Fetch materials for the subject
            materials = Materials.objects.filter(subject=subjectObject)

            if not materials.exists():
                return JsonResponse({"error": "No materials found for the subject"}, status=404)

            # Prepare a list of base64-encoded binary data for each file
            file_responses = []
            for material in materials:
                # Check if the material file is stored as bytes or a file-like object
                if isinstance(material.file, bytes):
                    # If the file is already a byte string, directly use it
                    file_content = material.file
                else:
                    # Otherwise, read the file content (in case it's a FileField)
                    file_content = material.file.read()  # Read the file content as bytes

                # Encode the binary data to base64 to transfer over JSON
                encoded_file_content = base64.b64encode(file_content).decode('utf-8')

                file_responses.append({
                    'file_content': encoded_file_content,  # Base64 encoded file content
                })

            return JsonResponse({
                "files": file_responses
            })

        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def addMaterial(request):
    if request.method == 'POST':
        try:
            subject = request.POST.get('subject')
            file = request.FILES.get('file')

            # Read the file content as bytes
            file_content = file.read()

            # Fetch the subject object
            subjectObject = Subject.objects.get(name=subject)

            # Create a new material and store the file as a byte string
            material = Materials.objects.create(subject=subjectObject, file=file_content)

            return JsonResponse({"message": "Material added successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def createTask(request : HttpRequest):
    if request.method == 'POST':
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            description = data.get('description')
            user = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            user = user[0]
            task = Tasks.objects.create(description=description, user=user, flag=False)
            return HttpResponse(task, status=201)
        except:
            return HttpResponse("Error", status=400)
@csrf_exempt
def getTasks(request : HttpRequest):
    jwt = JWTAuthentication()
    user = jwt.authenticate(request)
    if user is None:
        return HttpResponse("Authentication failed", status=401)
    user = user[0]
    tasks = Tasks.objects.filter(user=user)
    task_list = []
    for task in tasks:
        task_list.append({
            'id' : task.id,
            'description': task.description,
            'flag': task.flag
        })
    return JsonResponse({
        "tasks": task_list
    })
@csrf_exempt
def getAssignments(request : HttpRequest):
    if request.method == "POST":
        jwt = JWTAuthentication()
        user = jwt.authenticate(request)
        if user is None:
            return HttpResponse("Authentication failed", status=401)
        user = user[0]
        assignments = UserAssignment.objects.filter(user=user)
        assignments_list = []
        for assignment in assignments:
                assignment_data = {
                    'id': assignment.assignment.id,
                    'subject': assignment.assignment.subject.name,
                    'type': assignment.assignment.type.type,
                    'deadline': assignment.assignment.deadline,
                    'status': assignment.status.status,  # Assuming the status has a name field
                    'seen' : assignment.seen,
                    'description': assignment.assignment.description,
                }
                assignments_list.append(assignment_data)

        # Return the assignments in the response
        response_data = {
            'assignments': assignments_list,
        }
        return JsonResponse(response_data)
    else :
        return HttpResponse("Method not allowed", status=405)
@csrf_exempt
def deleteTask(request : HttpRequest):
    if request.method == 'POST':
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            id = data.get('id')
            user = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            user = user[0]
            task = Tasks.objects.get(id=id, user=user)
            if task is None:
                return HttpResponse("Task not found", status=404)
            task.delete()
            return HttpResponse("Task deleted", status=200)
        except:
            return HttpResponse("Error", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)
@csrf_exempt
def completeTask(request : HttpRequest):
    if request.method == 'POST':
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            id = data.get('id')
            user = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            user = user[0]
            task = Tasks.objects.get(id=id, user=user)
            task.flag = True
            task.save()
            return HttpResponse("Task completed", status=200)
        except:
            return HttpResponse("Error", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)
@csrf_exempt
def completeAssignment(request : HttpRequest):
    if request.method == "POST":
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            assignment_id = data.get('id')
            user = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            user = user[0]
            assignment = UserAssignment.objects.get(user=user, assignment_id=assignment_id)
            status_object = AssignmentStatus.objects.get(status="Submitted")
            assignment.status = status_object
            assignment.save()
            return HttpResponse("Assignment completed", status=200)
        except:
            return HttpResponse("Error", status=400)
       
@csrf_exempt
def deleteAssignment(request : HttpRequest):
    if request.method == "POST":
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            id = data.get('id')
            user = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            if not user[0].is_superuser:
                return HttpResponse("You are not authorized to delete assignments", status=403)
            user = user[0]
            assignment = Assignment.objects.get(id=id)
            assignment.delete()
            return HttpResponse("Assignment deleted", status=200)
        except Exception as e:
            return HttpResponse(str(e), status=400)

@csrf_exempt
def setAssignmentAsSeen(request : HttpRequest):
    print(json.loads(request.body))
    if request.method == "POST":
 
            jwt = JWTAuthentication()
            user , _ = jwt.authenticate(request)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            data = json.loads(request.body)
            idList = data.get('idList')
            for id in idList:
                assignObject = Assignment.objects.get(id=id)
                assignment = UserAssignment.objects.get(assignment=assignObject, user = user)
                assignment.seen = True
                assignment.save()
            return HttpResponse("Assignment marked as seen", status=200)
@csrf_exempt
def getSubjectList(request : HttpRequest):
    if request.method == "POST":
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("Method not allowed", status=405)
@csrf_exempt
def getNotifications(request : HttpRequest):
    if request.method == "POST":
        jwt = JWTAuthentication()
        user = jwt.authenticate(request)
        if user is None:
            return HttpResponse("Authentication failed", status=401)
        user = user[0]
        notifications = userNotification.objects.filter(user=user)
        notification_list = []
        for notification in notifications:
            if notification.seen == False:
                notification_list.append({
                    'title': notification.notification.title,
                    'description': notification.notification.description,
                    'seen': notification.seen
                })
        return JsonResponse({
            "notifications": notification_list
        })
    else:
        return HttpResponse("Method not allowed", status=405)
@csrf_exempt
def createNotification(request: HttpRequest):
    if request.method == 'POST':
        try:
            user , _ = JWTAuthentication().authenticate(request)
            if not user.is_superuser:
                return HttpResponse("You are not authorized to create notifications", status=403)
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            notification = Notification.objects.create(title=title, description=description)
            users = User.objects.all()
            for user in users:
                userNotification.objects.create(user=user, notification=notification, seen=False)
            return HttpResponse("Notification created", status=201)
        except:
            return HttpResponse("Error", status=400)
@csrf_exempt
def setNotificationAsSeen(request: HttpRequest):
    if request.method == "POST":
        jwt = JWTAuthentication()
        user, _ = jwt.authenticate(request)
        if user is None:
            return HttpResponse("Authentication failed", status=401)

        data = json.loads(request.body)
        idList = data.get('idList')

        if not idList:
            return HttpResponse("No notifications to delete", status=400)

        # Try to delete notifications
        for id in idList:
            try:
                # Fetch notification by its ID and the associated user
                notification = userNotification.objects.get(notification_id=id, user=user)
                print(f"Deleting notification: {notification}")
                
                # Delete the notification
                notification.delete()
                print(f"Notification with ID {id} deleted.")

            except userNotification.DoesNotExist:
                # If notification does not exist, log it
                print(f"Notification with ID {id} not found for user {user}")
                continue

        return HttpResponse("Notifications deleted successfully", status=200)
@csrf_exempt
def handleRequest(request : HttpRequest):
    # Manually authenticate using JWT
    auth = JWTAuthentication()
    user, _ = auth.authenticate(request)
    if user is None:
        return HttpResponse("Authentication failed", status=401)
    data = json.loads(request.body)
    query = data.get('query')
    handler = QueryHandler()
    response = handler.identify_query(query)
    if response == "create assignment" or response == "create notification" or response == "create material":
        if not user.is_superuser:
            return JsonResponse({
                 "response":"You are not authorized to do this action"}, status=403)
        else:
            return JsonResponse({
                "response":response
            }
            , status=200)
    else:
        return JsonResponse({
            "response":response
        },safe=False, status=200)
    