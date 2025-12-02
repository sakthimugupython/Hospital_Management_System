from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# User Profile Model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('pharmacist', 'Pharmacist'),
        ('lab_technician', 'Lab Technician'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"


# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=200, help_text="e.g., Mon, Wed, Fri")
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


# Patient Model
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    appointment_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.appointment_number} - {self.patient.get_full_name()} with Dr. {self.doctor.user.get_full_name()}"


# Ward/Bed Model
class Ward(models.Model):
    WARD_TYPE_CHOICES = [
        ('ICU', 'ICU'),
        ('General', 'General'),
        ('Private', 'Private'),
        ('Emergency', 'Emergency'),
    ]
    
    ward_name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPE_CHOICES)
    floor = models.IntegerField()
    total_beds = models.IntegerField()
    charge_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.ward_name} - {self.ward_type}"
    
    def available_beds(self):
        occupied = Bed.objects.filter(ward=self, status='occupied').count()
        return self.total_beds - occupied


class Bed(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]
    
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')
    
    class Meta:
        unique_together = ['ward', 'bed_number']
    
    def __str__(self):
        return f"{self.ward.ward_name} - Bed {self.bed_number}"


# IPD (In-Patient Department) Model
class IPDRecord(models.Model):
    STATUS_CHOICES = [
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ]
    
    ipd_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ipd_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField()
    treatment_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='admitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ipd_number} - {self.patient.get_full_name()}"


# OPD (Out-Patient Department) Model
class OPDRecord(models.Model):
    opd_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='opd_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    vitals_bp = models.CharField(max_length=20, blank=True, verbose_name="Blood Pressure")
    vitals_temperature = models.CharField(max_length=10, blank=True)
    vitals_pulse = models.CharField(max_length=10, blank=True)
    vitals_weight = models.CharField(max_length=10, blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.opd_number} - {self.patient.get_full_name()}"


# Medicine Model
class Medicine(models.Model):
    medicine_name = models.CharField(max_length=200)
    medicine_type = models.CharField(max_length=100, help_text="e.g., Tablet, Syrup, Injection")
    manufacturer = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medicine_name} - {self.medicine_type}"
    
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
    
    def needs_reorder(self):
        return self.stock_quantity <= self.reorder_level


# Pharmacy Prescription Model
class PharmacyPrescription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled'),
    ]
    
    prescription_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    opd_record = models.ForeignKey(OPDRecord, on_delete=models.SET_NULL, null=True, blank=True)
    ipd_record = models.ForeignKey(IPDRecord, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    dispensed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dispensed_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.prescription_number} - {self.patient.get_full_name()}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(PharmacyPrescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dosage = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.quantity}"


# Lab Test Model
class LabTest(models.Model):
    test_name = models.CharField(max_length=200)
    test_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    normal_range = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.test_code} - {self.test_name}"


# Lab Test Request Model
class LabTestRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    result = models.TextField(blank=True)
    report_file = models.FileField(upload_to='lab_reports/', null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.request_number} - {self.patient.get_full_name()} - {self.test.test_name}"


# Billing Model
class Bill(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('insurance', 'Insurance'),
    ]
    
    bill_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    opd_record = models.ForeignKey(OPDRecord, on_delete=models.SET_NULL, null=True, blank=True)
    ipd_record = models.ForeignKey(IPDRecord, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Charges
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicine_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.subtotal = (
            self.consultation_fee + 
            self.room_charges + 
            self.medicine_charges + 
            self.lab_charges + 
            self.other_charges
        )
        self.total_amount = self.subtotal - self.discount + self.tax
        self.balance = self.total_amount - self.amount_paid
        
        if self.balance == 0:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bill_number} - {self.patient.get_full_name()}"


# Staff Attendance Model
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date} - {self.status}"


# Staff Shift Model
class Shift(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning (6 AM - 2 PM)'),
        ('afternoon', 'Afternoon (2 PM - 10 PM)'),
        ('night', 'Night (10 PM - 6 AM)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = ['user', 'shift_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.shift_type} - {self.shift_date}"


# Medical Report Model
class MedicalReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('lab', 'Lab Report'),
        ('radiology', 'Radiology'),
        ('prescription', 'Prescription'),
        ('discharge', 'Discharge Summary'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_file = models.FileField(upload_to='medical_reports/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.title}"
