from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Institution, Student, AcademicInfo, StudentDocument
from django.http import JsonResponse
import qrcode
import os
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth.models import User
from django.conf import settings

def home(request):
    if request.user.is_authenticated:
        return redirect('institution_dashboard')
    return render(request, 'student/home.html')

def institution_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('institution_dashboard')
    return render(request, 'student/institution_login.html')

def institution_dashboard(request):
    institution = Institution.objects.get(user=request.user)
    students = institution.students.all()
    return render(request, 'student/institution_dashboard.html', {'students': students, 'institution': institution})

def create_student(request):
    if request.method == "POST":
        name = request.POST['name']
        dob = request.POST['dob']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        batch = request.POST['batch']
        branch = request.POST['branch']
        institution = Institution.objects.get(user=request.user)

        # Create a new User for the student
        user = User.objects.create_user(username=phone_number, email=email, password='temporary_password')

        # Create the Student record and associate the User
        student = Student.objects.create(
            user=user,
            institution=institution,
            name=name,
            dob=dob,
            email=email,
            phone_number=phone_number,
            batch=batch,
            branch=branch
        )

        student.save()
        return redirect('institution_dashboard')

    return render(request, 'student/create_student.html')


from django.utils.timezone import now

def verify_student_qr(request, student_id, otp):
    try:
        student = Student.objects.get(id=student_id)

        # Check if OTP matches and is valid
        if student.otp != otp:
            return JsonResponse({'error': 'Invalid OTP'}, status=403)

        # Regenerate OTP for the next use
        student.otp = student.generate_otp()
        student.save(force_qr_update=False)  # Update OTP without regenerating QR code

        # Fetch student data for display
        academic_info = student.academic_info.all()
        documents = student.documents.all()
        return render(request, 'student/student_details.html', {'student': student, 'academic_info': academic_info, 'documents': documents})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)


def verify_otp(request, student_id, otp):
    try:
        student = Student.objects.get(id=student_id)

        # Check OTP for institution users
        if student.otp != otp:
            return JsonResponse({'error': 'Invalid OTP'}, status=403)

        # Redirect to the dashboard if OTP is correct
        academic_info = student.academic_info.all()
        documents = student.documents.all()
        return render(request, 'student/student_details.html', {'student': student, 'academic_info': academic_info, 'documents': documents})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    try:
        student = Student.objects.get(id=student_id)
        academic_info = student.academic_info.all()
        documents = student.documents.all()
        return render(request, 'student/student_details.html', {'student': student, 'academic_info': academic_info, 'documents': documents})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

def scan_qr(request):
    if request.method == 'POST':
        # Handle QR scanning logic (e.g., use a library to decode QR and retrieve student ID)
        qr_data = request.POST.get('qr_data')  # Get the data from scanned QR code
        student_id = int(qr_data.split(':')[2].strip())  # Assuming QR data includes the student ID

        # Verify and show student data
        try:
            student = Student.objects.get(id=student_id)
            academic_info = student.academic_info.all()
            documents = student.documents.all()
            return render(request, 'student/student_details.html', {'student': student, 'academic_info': academic_info, 'documents': documents})
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

    return render(request, 'student/scan_qr.html')
from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
from datetime import timedelta
from django.utils.timezone import now

def view_student_details(request, student_id):
    try:
        student = Student.objects.get(id=student_id)

        academic_info = student.academic_info.all()
        documents = student.documents.all()

        return render(request, 'student/student_details.html', {
            'student': student,
            'academic_info': academic_info,
            'documents': documents,
        })

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Student, AcademicInfo, Institution

@login_required
def add_academic_info(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Check if the logged-in user's institution is the same as the student's institution
    if request.user.institution != student.institution.user.institution:
        return HttpResponseForbidden("You do not have permission to add academic details for this student.")

    if request.method == "POST":
        course_name = request.POST.get('course_name')
        grade = request.POST.get('grade')
        semester = request.POST.get('semester')
        document = request.FILES.get('document')

        # Create academic info for the student, no need to pass 'institution' explicitly
        AcademicInfo.objects.create(
            student=student,
            course_name=course_name,
            grade=grade,
            semester=semester,
            document=document
        )
        return redirect('student_details', student_id=student.id)

    return render(request, 'student/add_academic_info.html', {'student': student})


@login_required
def edit_student(request, student_id):
    # Get the student object
    student = get_object_or_404(Student, id=student_id)

    # Check if the logged-in institution is associated with the student
    if student.institution.user != request.user:
        return redirect('unauthorized')  # Redirect to an unauthorized page if the institution doesn't match

    if request.method == 'POST':
        # Update the student details with data from the POST request
        student.name = request.POST.get('name', student.name)
        student.dob = request.POST.get('dob', student.dob)
        student.email = request.POST.get('email', student.email)
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.batch = request.POST.get('batch', student.batch)
        student.branch = request.POST.get('branch', student.branch)

        # Optionally handle the file upload for QR code or other fields
        student.save()

        # Redirect to the student details page after saving
        return redirect('view_student', student_id=student.id)

    return render(request, 'student/edit_student.html', {'student': student})

from django.contrib.auth import logout

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')
