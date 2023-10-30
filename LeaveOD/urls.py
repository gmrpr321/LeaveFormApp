from .views import(
    LoginUser,
    LogoutUser,
    CreateUser,
    RetriveUser,
    UpdateUser,
    RetriveStudentFormByID,
    StudentCreateForm,
    StaffViewForm,
    ValidateForm,
    RetriveStudentFormsForClassIncharge,
    RetriveStudentFormsForMentor,
    RetriveStudentFormsForHOD
)

from django.urls import path 
urlpatterns = [
    path('Login/',LoginUser.as_view(),name="Login"),
    path('Logout/',LogoutUser.as_view(),name = "Logout"),
    path('CreateUser/',CreateUser.as_view(),name = "CreateUser"),
    path('RetriveUser/<str:pk>/',RetriveUser.as_view(),name = "RetriveUser"),
    path('UpdateUser/<str:pk>/',UpdateUser.as_view(),name = "UpdateUser"),
    path('RetriveStudentFormsById/<str:student_id>/',RetriveStudentFormByID.as_view(),name = "RetriveStudentFormsById"),
    path('StudentCreateForm/',StudentCreateForm.as_view(),name = "StudentCreateForm"),
    path('StaffViewForm/',StaffViewForm.as_view(),name = "StaffViewForm"),
    path('ValidateForm/',ValidateForm.as_view(),name = "ValidateForm"),
    path('RetriveStudentFormsForClassIncharge/<str:class_incharge_id>/<str:date_from>/<str:date_to>/',RetriveStudentFormsForClassIncharge.as_view(),name = "RetriveStudentFormsForClassIncharge"),
    path('RetriveStudentFormsForMentor/<str:mentor_id>/<str:date_from>/<str:date_to>/',RetriveStudentFormsForMentor.as_view(),name='RetriveStudentFormsForMentor'),
    path('RetriveStudentFormsForHOD/<str:HOD_id>/<str:date_from>/<str:date_to>/',RetriveStudentFormsForHOD.as_view(),name='RetriveStudentFormsForHOD')

]
