from django.shortcuts import render
from .models import User, Form
from .serializers import UserSerializer, FormSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request as RestRequest
from django.http.request import HttpRequest
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    GenericAPIView
)
from django.http import HttpRequest
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

from rest_framework.parsers import MultiPartParser,FileUploadParser

from rest_framework.decorators import permission_classes,api_view

import pandas as pd

from django.utils.decorators import method_decorator

class LoginUser(APIView):

    permission_classes = []
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            return Response(
                {"is_staff": user.is_staff, "username": user.username},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutUser(APIView):
    permission_classes = []
    def get(self, request: RestRequest):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class CreateUser(CreateAPIView):
    """
    Create a new user. Applicable for both staff and students
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetriveUser(RetrieveAPIView):
    """
    Retrive the data of a specific user
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class UpdateUser(UpdateAPIView):
    """
    Update the data of a specific user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetriveStudentFormsForStaff(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: RestRequest):
        """
        Given is a ID of staff, Return the JSON containing all the leave forms per student
        """
        student_data = []
        # find the set of students that have the staff as mentor/class Incharge
        student_mentor_set = User.objects.filter(mentor=request.user.username)
        student_class_set = User.objects.filter(class_incharge=request.user.username)
        # combine the two sets
        students = student_mentor_set.union(student_class_set)
        # iterate the queryset to find the form models per student
        for student in students:
            # find the form models
            current_student_data = {"name": student.name}
            student_form_set = Form.objects.filter(student_id=student.username)
            # now for each form of a single student, serialize it and store it
            form_data = []
            for form in student_form_set:
                serialized_form_data = FormSerializer(form)
                form_data.append(serialized_form_data)
            current_student_data["forms"] = form_data
            student_data.append(current_student_data)
        return Response(student_data, status=status.HTTP_200_OK)


class RetriveStudentFormByID(APIView):
    permission_classes =[]
    def get(self, request, *args,**kwargs):
        """
        Given is a student_id, return a list of forms submitted by that student
        """
        forms = Form.objects.filter(student=str(kwargs['username']))
        # serialize each form object
        serialized_forms = []
        for form in forms:
            serialized_forms.append(FormSerializer(form).data)
        return Response(serialized_forms, status=status.HTTP_200_OK)


# creation of the application form to apply leave or onduty on the portal
class StudentCreateForm(CreateAPIView):
    permission_classes = []
    serializer_class = FormSerializer
    queryset = Form.objects.all()


# updation of the application form in the fields like Parent_consent , staff_confirmation , HOD_confirmation
class StaffUpdateViewForm(RetrieveUpdateAPIView):
    # uses form.id

    permission_classes = []

    serializer_class = FormSerializer
    queryset = Form.objects.all()
    lookup_field = "id"
    
    def update(self,request :RestRequest,*args,**kwargs):
        try :
            student_mentor = User.objects.filter(mentor = request.user.username)
            student_CI = User.objects.filter(class_incharge = request.user.username)
            student_set = student_mentor.union(student_CI)

            for student in student_set:
                form_data = Form.objects.get(student_name = student.username,id = kwargs[id])
                serializer_form = FormSerializer(form_data,data = request.data,partial = True)
                serializer_form.is_valid()
                print(serializer_form.error_messages)
                self.perform_update(serializer_form.data)

                if serializer_form.data['HOD_confirmation'] == True:
                    if request.user.is_HOD == True:
                        return Response(serializer_form.data,status=status.HTTP_200_OK)
                    else :
                        context = {
                            "message" : "HOD should only access that field no other should access the field"
                        }
                        return Response(data = context , status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer_form.data,status=status.HTTP_200_OK)
            

        except Exception as e:
            print("following exception occured:",e)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


class CreateUserbyExcel(APIView):
    parser_classes = (FileUploadParser,)

    permission_classes = [IsAdminUser]
    def post(self,request,format=None):
        excel_file = request.data['excel_file']

        try:
            df = pd.read_excel(excel_file)
            data = df.to_dict(orient = 'records')

            for record in data:
                User.objects.create(**record)

            return Response({'message':'user created successfully via excel'})
        except Exception as e:
            return Response({'error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
         


# class validateFormByStaff(APIView):
