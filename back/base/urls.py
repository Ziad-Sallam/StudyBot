from django.urls import path
from .views import *

urlpatterns= [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('handle-request',handleRequest,name="handle"),
    path('create-assignment',createAssignment,name="create-assignment"),
    path('get-materials',getMaterial,name="get-material"),
    path('add-material',addMaterial,name="add-material"),
    path('create-task',createTask,name="create-task"),
    path('get-tasks',getTasks,name="get-tasks"),
    path('get-assignments',getAssignments,name="get-assignments"),
    path('delete-task',deleteTask,name="delete-task"),
    path('complete-task',completeTask,name="complete-task"),
    path('complete-assignment',completeAssignment,name="complete-assignment"),
    path('delete-assignment',deleteAssignment,name="delete-assignment"),
    path('set-seen', setAssignmentAsSeen, name="set-seen"),
    path('get-subjects',getSubjectList,name="get-subjects"),
]