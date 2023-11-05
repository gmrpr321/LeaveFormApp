from django.shortcuts import render
from .models import AppUser, Form
from django.contrib.auth.models import User
from .serializers import AppUserSerializer, FormSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request as RestRequest
from django.http.request import HttpRequest
from datetime import datetime
from django.db.models import Q
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
        # corresponding appuser object
        appuser = AppUser.objects.get(user=user)
        print(user)
        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            return Response(
                {"is_staff": appuser.is_staff,"is_hod" : appuser.is_hod, "username": user.username},
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


class CreateUser(APIView):
    """
    Create a new user. Applicable for both staff and students.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.pop('username')
        password = request.data.pop('password')
        
        # Check if the username and password are provided
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new User
        try:
            user_obj = User.objects.create_user(username=username, password=password)
            user_obj.save()
        except:
            return Response({"error" : "Unable to Create User"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # Serialize the user data
        app_user_object_serializer = AppUserSerializer(data={"user":user_obj.pk,**request.data})
        
        if app_user_object_serializer.is_valid():
            app_user_object_serializer.save()
            return Response(app_user_object_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(app_user_object_serializer.errors)
            return Response(app_user_object_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveUser(RetrieveAPIView):
    """
    Retrive the data of a specific user
    """

    serializer_class = AppUserSerializer
    queryset = User.objects.all()


class UpdateUser(UpdateAPIView):
    """
    Update the data of a specific user
    """

    serializer_class = AppUserSerializer
    queryset = User.objects.all()


class RetriveStudentFormsForStaffandMentor(APIView):
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
    
class RetriveStudentFormsForHOD(APIView):
    def get(self,request,HOD_id,date_from,date_to):
        """
       Given is a student_id, return a list of forms that belongs to this HOD
       that are within this specified date range 
        """
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            return Response({"Details": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        if date_from <=date_to:
            # fIND the Queryset of students that belong to this HOD
            students_set = AppUser.objects.filter(HOD_username=HOD_id)
            # for every single student found, their associated forms
            parsed_forms= []
            for student in students_set:
                student_forms = Form.objects.filter(student=student.user.username)
                # now only select the forms in the specified time range
                student_forms = student_forms.filter(Q(date_from__gte=date_from) & Q(date_to__lte=date_to))
                # serialize the given forms
                for student_form in student_forms:
                    parsed_forms.append(FormSerializer(student_form).data)
            return Response(parsed_forms,status=status.HTTP_200_OK)
        return Response({"Details" : "Invalid Time Range"},status=status.HTTP_400_BAD_REQUEST)

class RetriveStudentFormsForMentor(APIView):
    def get(self,request,mentor_id,date_from,date_to):
        """
       Given is a student_id, return a list of forms that belongs to this mentor
       that are within this specified date range 
        """
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            return Response({"Details": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        if date_from <=date_to:
            # fIND the Queryset of students that belong to this mentor
            students_set = AppUser.objects.filter(mentor_username=mentor_id)
            # for every single student found, their associated forms
            parsed_forms= []
            for student in students_set:
                student_forms = Form.objects.filter(student=student.user.username)
                # now only select the forms in the specified time range
                student_forms = student_forms.filter(Q(date_from__gte=date_from) & Q(date_to__lte=date_to))
                # serialize the given forms
                for student_form in student_forms:
                    parsed_forms.append(FormSerializer(student_form).data)
            return Response(parsed_forms,status=status.HTTP_200_OK)
        return Response({"Details" : "Invalid Time Range"},status=status.HTTP_400_BAD_REQUEST)

class RetriveStudentFormsForClassIncharge(APIView):
    def get(self,request,class_incharge_id,date_from,date_to):
        """
       Given is a student_id, return a list of forms that belongs to this class incharge
       that are within this specified date range 
        """
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            return Response({"Details": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        if date_from <=date_to:
            # fIND the Queryset of students that belong to this class Incharge
            students_set = AppUser.objects.filter(class_incharge_username=class_incharge_id)
            # for every single student found, their associated forms
            parsed_forms= []
            for student in students_set:
                student_forms = Form.objects.filter(student=student.user.username)
                # now only select the forms in the specified time range
                student_forms = student_forms.filter(Q(date_from__gte=date_from) & Q(date_from__lte=date_to))
                # serialize the given forms
                for student_form in student_forms:
                    parsed_forms.append(FormSerializer(student_form).data)
            return Response(parsed_forms,status=status.HTTP_200_OK)
        return Response({"Details" : "Invalid Time Range"},status=status.HTTP_400_BAD_REQUEST)

class RetriveStudentFormByID(APIView):
    def get(self, request, student_id):
        """
        Given is a student_id, return a list of forms submitted by that student
        """
        forms = Form.objects.filter(student=student_id)
        # serialize each form object
        serialized_forms = []
        for form in forms:
            serialized_forms.append(FormSerializer(form).data)
        return Response(serialized_forms, status=status.HTTP_200_OK)


# creation of the application form to apply leave or onduty on the portal
class StudentCreateForm(CreateAPIView):
    # def post(self,request):
    #     serialier = FormSerializer(data=request.data)
    #     serialier.is_valid()
    #     print(serialier.errors)
    serializer_class = FormSerializer
    queryset = Form.objects.all()


# updation of the application form in the fields like Parent_consent , staff_confirmation , HOD_confirmation
class StaffViewForm(UpdateAPIView):
    # uses form.id
    serializer_class = FormSerializer
    queryset = Form.objects.all()


class ValidateForm(APIView):
    """
    Given is a form_ID and a position that validates this form (enum{'class_Incharge','HoD','mentor'})
    validate the form for this respective position

    Also validate the parent consent if applicable
    payload:{
    form_id : string,
    position : string enum{'class_Incharge','HoD','mentor'}
    is_parent_validate : bool
    is_staff_validate : bool
    } 
    """
    
    def post(self,request):
        # find the corresponding form object
        data = request.data
        print(data)
        form_object = Form.objects.get(id=data.get('id'))
        if(form_object):
            # mark the position consent as true
            if(data['position']=='class_Incharge'):
                form_object.is_staff_consent = data.get('is_staff_validate')
            elif(data['position']=='HoD'):
                form_object.is_HOD_consent = data.get('is_staff_validate')
            elif(data['position']=='mentor'):
                form_object.is_staff_consent = data.get('is_staff_validate')
            # check for parent consent
            form_object.is_parent_consent = data.get('is_parent_validate')
            print(data)
            print(form_object.is_parent_consent,form_object.is_staff_consent,form_object.is_HOD_consent)
            form_object.save()
            return Response({"data" : "Saved_Successfully"},status=status.HTTP_200_OK)
        return Response({"data" : "Invalid Form ID"},status=status.HTTP_400_BAD_REQUEST)
    