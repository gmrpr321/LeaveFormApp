# from .views import (
#     StaffFormView,
#     StudentFormView,
#     AllFormView,
#     DisplayStudentFormView,
#     UserEditView,
# )

from django.urls import path 
from .views import LoginUser,LogoutUser,StaffUpdateViewForm,StudentCreateForm,RetriveStudentFormByID,RetriveStudentFormsForStaff,CreateUser,RetriveUser,UpdateUser,CreateUserbyExcel



urlpatterns = [
    # path('StudentLeaveForm/',StudentFormView.as_view(),name="StudentFormView"),
    # path('StaffUpdateForm/',StaffFormView.as_view(),name = "StaffFormView"),
    # path('LeaveFormList/',AllFormView.as_view(),name = "AllFormView"),
    # path('LeaveForm/<str:student_id>/',DisplayStudentFormView.as_view(),name = "DisplayStudentFormView"),
    # path('EditMentor/',UserEditView.as_view(),name = "UserEditView"),
    path('Login/',LoginUser.as_view(),name = "login"),
    path('Logout/',LogoutUser.as_view(),name = "logout"),
    path('CreateUser/',CreateUser.as_view(),name = "create new user"),
    path('RetrieveUser/<str:username>',RetriveUser.as_view(),name = "retrieve user details"),
    path('UpdateUser/',UpdateUser.as_view(),name = "update user"),
    path('RetrieveStudentFormsForStaffs/',RetriveStudentFormsForStaff.as_view(),name = "retrieve form"),
    path('SelectFormById/<str:username>',RetriveStudentFormByID.as_view(),name = "retrieve form by id"),
    path('ViewForm/<int:id>',StaffUpdateViewForm.as_view(),name = "view form for staff"),
    path('CreateForm/',StudentCreateForm.as_view(),name = "create form for student"),
    path('CreateUserExcel',CreateUserbyExcel.as_view(),name = "create a new user via excel"),
]
