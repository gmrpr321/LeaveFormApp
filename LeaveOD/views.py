from django.shortcuts import render
from .models import User,Form
from .serializers import AuthenticationSerializer,FormSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
# Create your views here.

# creation of the application form to apply leave or onduty on the portal
class StudentFormView(CreateAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()
    
# updation of the application form in the fields like Parent_consent , staff_confirmation , HOD_confirmation
class StaffFormView(UpdateAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

# Here the respective mentors or class incharges can view all leave applications of their respective students
class AllFormView(ListAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

# here the respective mentors or class incharges can view the particular or single leave application 
class DisplayStudentFormView(RetrieveAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

#we can edit user details as if there is a change in the mentor of the student
class UserEditView(UpdateAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

