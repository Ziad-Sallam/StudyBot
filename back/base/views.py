import base64
import json
import os
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
import google.generativeai as genai




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
    

def createAssignment(subject, assignment_type, deadline, description):
    
    subjectObject = Subject.objects.get(name=subject)
    assignmentTypeObject = AssignmentType.objects.get(type=assignment_type)
    pendingStatus = AssignmentStatus.objects.get(id=2)  # Assuming id 2 is for "Pending" status

    assignment = Assignment.objects.create(subject=subjectObject, type=assignmentTypeObject, deadline=deadline, description=description)
    # Create a UserAssignment for each user with the new assignment and pending status
    users = User.objects.all()
    for user in users:
        UserAssignment.objects.create(user=user, assignment=assignment, status=pendingStatus)

            
@csrf_exempt
def getMaterial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get('subject')

            if not subject:
                return JsonResponse({"error": "Subject is required"}, status=400)

            # Get the subject object
            subject_object = Subject.objects.get(name=subject)

            # Fetch materials for the subject
            materials = Materials.objects.filter(subject=subject_object)

            if not materials.exists():
                return JsonResponse({"error": "No materials found for the subject"}, status=404)
            
            # Prepare a list of material IDs
            material_responses = []
            for material in materials:
                file_name, file_extension = os.path.splitext(os.path.basename(material.file.name))
                material_responses.append({
                    'id': material.id,
                    "name" : file_name,
                    "type" : file_extension.lstrip('.').lower()
                })

            return JsonResponse({
                "materials": material_responses
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
            print(file)
            print(subject)

            if not subject or not file:
                return JsonResponse({"error": "Subject and file are required"}, status=400)

            # Fetch the subject object
            subject_object = Subject.objects.get(name=subject)

            # Create a new material and save the file
            material = Materials.objects.create(subject=subject_object, file=file)

            return JsonResponse({
                "message": "Material added successfully",
                "id": material.id,
                "file_path": material.file.url
            }, status=201)

        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def getMaterialData(request: HttpRequest):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            material_id = data.get('id')

            if not material_id:
                return JsonResponse({"error": "Material ID is required"}, status=400)

            # Fetch the material object
            material = Materials.objects.get(id=material_id)

            # Read the file content
            file_path = material.file.path
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Encode the file content in base64 for safe JSON transfer
            encoded_file_content = base64.b64encode(file_content).decode('utf-8')

            return JsonResponse({
                "id": material.id,
                "file_name": material.file.name,  # Include the file name
                "file_data": encoded_file_content  # Base64 encoded file content
            })

        except Materials.DoesNotExist:
            return JsonResponse({"error": "Material not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
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
def completeAssignment(request: HttpRequest):
    if request.method == "POST":
        try:
            jwt = JWTAuthentication()
            data = json.loads(request.body)
            assignment_id = data.get('id')
            print(assignment_id)
            print(assignment_id)
            user = jwt.authenticate(request)
            print(assignment_id)
            if user is None:
                return HttpResponse("Authentication failed", status=401)
            print(assignment_id)
            user = user[0]
            print(assignment_id)
            assignment = UserAssignment.objects.get(user=user, assignment_id=assignment_id)
            print(assignment_id)
            status_object = AssignmentStatus.objects.get(status="Submitted")
            print(assignment_id)
            assignment.status = status_object

            assignment.save()
            return HttpResponse("Assignment back to pending", status=200)
        except:
            return HttpResponse("Error", status=400)

@csrf_exempt
def uncompleteAssignment(request: HttpRequest):
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
            status_object = AssignmentStatus.objects.get(status="Pending")
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
                    'id': notification.notification.id,
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
    print(response)
    if response == "create assignment" or response == "create notification" or response == "create material":
        if not user.is_superuser:
            return JsonResponse({
                 "response":"You are not authorized to do this action"}, status=403)
        else:
            if response == "create assignment":
                subject, deadline, description, type_id = handler.get_assignment_description(query)
                createAssignment(subject, type_id, deadline, description)
                return JsonResponse({
                    "response": f"Assignment '{description}' created successfully"
                }, safe=False, status=200)
            
            elif response == "create notification":
                title, description = handler.get_notification_description(query)
                notification = Notification.objects.create(title=title, description=description)
                users = User.objects.all()
                for user in users:
                    userNotification.objects.create(user=user, notification=notification, seen=False)
                return JsonResponse({
                    "response": f"Notification '{title}' created successfully with description '{description}'"
                }, safe=False, status=200)
            

            return JsonResponse({
                "response": f"{response}"
            }, safe=False, status=200)
    
    if response == "create task":
        description = handler.get_task_description(query)
        task = Tasks.objects.create(description=description, user=user, flag=False)
        return JsonResponse({
            "response": f"Task created successfully with description: {description}"
        }, safe=False, status=200)
    
    if response not in ["create assignment", "create notification", "create material", "create task", "get assignment", "get tasks", "get assignments", "get subjects", "get notifications"]:
        return JsonResponse({
            "response": response
        }, safe=False, status=200)
    else:
        return JsonResponse({
            "response":response
        },safe=False, status=200)





