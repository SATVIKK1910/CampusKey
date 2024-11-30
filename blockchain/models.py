from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import os
import secrets
import string
import hashlib
from datetime import datetime
from django.conf import settings
# Custom storage system to save QR codes
qr_storage = FileSystemStorage(location=os.path.join('media', 'qr_codes'))

class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, related_name="students", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    sid = models.CharField(max_length=15, default='000000')
    batch = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', storage=qr_storage, null=True, blank=True)
    secure_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def generate_qr_code(self):
        """Generate QR code with secure URL and OTP."""
        self.secure_url = f"127.0.0.1:8000/student/details/{self.id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(self.secure_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        filename = f"student_{self.id}_qr.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        buffer.close()


    def save(self, *args, **kwargs):
        if not self.qr_code or kwargs.pop('force_qr_update', False):
            self.generate_qr_code()
        super().save(*args, **kwargs)

class AcademicInfo(models.Model):
    student = models.ForeignKey(Student, related_name="academic_info", on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=5)
    semester = models.CharField(max_length=20)
    document = models.FileField(upload_to='academic_documents/', null=True, blank=True)

    def __str__(self):
        return f"{self.course_name} - {self.grade}"

class StudentDocument(models.Model):
    student = models.ForeignKey(Student, related_name="documents", on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    document_file = models.FileField(upload_to='student_documents/')

    def __str__(self):
        return f"{self.document_type} - {self.student.name}"
