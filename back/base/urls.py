from django.urls import path
from .views import *

urlpatterns= [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('handle-request',handleRequest,name="handle")
]