from django.urls import path
from . import views

urlpatterns = [
    path('institution/login/', views.institution_login, name='institution_login'),
    path('institution/dashboard/', views.institution_dashboard, name='institution_dashboard'),
    path('student/create/', views.create_student, name='create_student'),
    # path('student/verify/<int:student_id>/', views.verify_student_qr, name='verify_student_qr'),
    path('student/scan_qr/', views.scan_qr, name='scan_qr'),
    path('student/verify/<int:student_id>/<str:otp>/', views.verify_student_qr, name='verify_student_qr'),
    path('student/otp/<int:student_id>/<str:otp>/', views.verify_otp, name='verify_otp'),
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('student/details/<uuid:student_id>', views.view_student_details, name='student_details'),
    path('student/verify/<uuid:student_id>/<str:otp>/', views.verify_student_qr, name='verify_student_qr'),
    path('student/<uuid:student_id>/add-academic/', views.add_academic_info, name='add_academic_info'),
    path('student/<uuid:student_id>/edit/', views.edit_student, name='edit_student'),


]
