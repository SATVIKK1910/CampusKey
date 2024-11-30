from django.contrib import admin
from .models import Institution, Student, AcademicInfo, StudentDocument

admin.site.register(Institution)
admin.site.register(Student)
admin.site.register(AcademicInfo)
admin.site.register(StudentDocument)
