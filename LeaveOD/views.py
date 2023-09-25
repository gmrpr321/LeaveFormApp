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
    UpdateAPIView,
)
from django.http import HttpRequest
from rest_framework import status
from django.contrib.auth import authenticate, login, logout


class LoginUser(APIView):
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
    def get(self, request: RestRequest):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class CreateUser(CreateAPIView):
    """
    Create a new user. Applicable for both staff and students
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetriveUser(RetrieveAPIView):
    """
    Retrive the data of a specific user
    """

    serializer_class = FormSerializer
    queryset = User.objects.all()


class UpdateUser(UpdateAPIView):
    """
    Update the data of a specific user
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RetriveStudentFormsForStaff(APIView):
    def get(self, request: RestRequest, staff_id):
        """
        Given is a ID of staff, Return the JSON containing all the leave forms per student
        """
        student_data = []
        # find the set of students that have the staff as mentor/class Incharge
        student_mentor_set = User.objects.filter(mentor=staff_id)
        student_class_set = User.objects.filter(class_incharge=staff_id)
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
    def get(self, request, student_id):
        """
        Given is a student_id, return a list of forms submitted by that student
        """
        forms = Form.objects.filter(student_id=student_id)
        # serialize each form object
        serialized_forms = []
        for form in forms:
            serialized_forms.append(FormSerializer(form))
        return Response(forms, status=status.HTTP_200_OK)


# creation of the application form to apply leave or onduty on the portal
class StudentCreateForm(CreateAPIView):
    serializer_class = FormSerializer
    queryset = Form.objects.all()


# updation of the application form in the fields like Parent_consent , staff_confirmation , HOD_confirmation
class StaffViewForm(UpdateAPIView):
    # uses form.id
    serializer_class = FormSerializer
    queryset = Form.objects.all()


# class validateFormByStaff(APIView):
