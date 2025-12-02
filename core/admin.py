from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Ward)
admin.site.register(Bed)
admin.site.register(IPDRecord)
admin.site.register(OPDRecord)
admin.site.register(Medicine)
admin.site.register(PharmacyPrescription)
admin.site.register(PrescriptionItem)
admin.site.register(LabTest)
admin.site.register(LabTestRequest)
admin.site.register(Bill)
admin.site.register(Attendance)
admin.site.register(Shift)
admin.site.register(MedicalReport)
