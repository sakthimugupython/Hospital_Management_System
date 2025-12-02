from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from .models import *
from .decorators import (
    admin_required, doctor_required, receptionist_required,
    nurse_required, pharmacist_required, lab_technician_required,
    patient_required, role_required
)
import random
import string

# Helper function to generate unique IDs
def generate_unique_id(prefix, length=8):
    return prefix + ''.join(random.choices(string.digits, k=length))

# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Role-based redirect
            try:
                role = user.profile.role
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'doctor':
                    return redirect('doctor_dashboard')
                elif role == 'receptionist':
                    return redirect('receptionist_dashboard')
                elif role == 'nurse':
                    return redirect('nurse_dashboard')
                elif role == 'pharmacist':
                    return redirect('pharmacist_dashboard')
                elif role == 'lab_technician':
                    return redirect('lab_technician_dashboard')
                elif role == 'patient':
                    return redirect('patient_dashboard')
            except:
                pass
            
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Dashboard View - Role-based redirect
@login_required
def dashboard(request):
    try:
        role = request.user.profile.role
        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'doctor':
            return redirect('doctor_dashboard')
        elif role == 'receptionist':
            return redirect('receptionist_dashboard')
        elif role == 'nurse':
            return redirect('nurse_dashboard')
        elif role == 'pharmacist':
            return redirect('pharmacist_dashboard')
        elif role == 'lab_technician':
            return redirect('lab_technician_dashboard')
        elif role == 'patient':
            return redirect('patient_dashboard')
    except:
        pass
    
    return redirect('admin_dashboard')

# Admin Dashboard
@login_required
@admin_required
def admin_dashboard(request):
    context = {}
    
    # Statistics
    context['total_patients'] = Patient.objects.count()
    context['total_doctors'] = Doctor.objects.count()
    context['appointments_today'] = Appointment.objects.filter(
        appointment_date=timezone.now().date()
    ).count()
    
    # Available beds
    total_beds = Bed.objects.count()
    occupied_beds = Bed.objects.filter(status='occupied').count()
    context['available_beds'] = total_beds - occupied_beds
    
    # Revenue statistics
    today = timezone.now().date()
    context['today_revenue'] = Bill.objects.filter(
        created_at__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Monthly revenue
    first_day_month = today.replace(day=1)
    context['monthly_revenue'] = Bill.objects.filter(
        created_at__date__gte=first_day_month
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent appointments
    context['recent_appointments'] = Appointment.objects.select_related(
        'patient', 'doctor__user'
    ).order_by('-created_at')[:5]
    
    # Pending tasks
    context['pending_appointments'] = Appointment.objects.filter(status='pending').count()
    context['pending_lab_tests'] = LabTestRequest.objects.filter(status='pending').count()
    context['low_stock_medicines'] = Medicine.objects.filter(
        stock_quantity__lte=models.F('reorder_level')
    ).count()
    
    # IPD patients
    context['ipd_patients'] = IPDRecord.objects.filter(status='admitted').count()
    context['user_role'] = 'admin'
    
    return render(request, 'dashboard.html', context)

# Doctor Dashboard
@login_required
@doctor_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'Doctor profile not found.')
        return redirect('logout')
    
    today = timezone.now().date()
    
    context = {
        'doctor': doctor,
        'total_patients': Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().count(),
        'total_doctors': 1,
        'appointments_today': Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).count(),
        'available_beds': Bed.objects.filter(status='vacant').count(),
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(
            doctor=doctor,
            status='admitted'
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            doctor=doctor,
            status='pending'
        ).count(),
        'pending_lab_tests': LabTestRequest.objects.filter(
            doctor=doctor,
            status='pending'
        ).count(),
        'low_stock_medicines': 0,
        'recent_appointments': Appointment.objects.filter(
            doctor=doctor
        ).select_related('patient', 'doctor__user').order_by('-created_at')[:5],
        'today': today,
        'user_role': 'doctor'
    }
    
    return render(request, 'dashboard.html', context)

# Receptionist Dashboard
@login_required
@receptionist_required
def receptionist_dashboard(request):
    today = timezone.now().date()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'appointments_today': Appointment.objects.filter(
            appointment_date=today
        ).count(),
        'available_beds': Bed.objects.filter(status='vacant').count(),
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(status='admitted').count(),
        'pending_appointments': Appointment.objects.filter(
            status='pending'
        ).count(),
        'pending_lab_tests': LabTestRequest.objects.filter(
            status='pending'
        ).count(),
        'low_stock_medicines': 0,
        'recent_appointments': Appointment.objects.select_related(
            'patient', 'doctor__user'
        ).order_by('-created_at')[:5],
        'today': today,
        'user_role': 'receptionist'
    }
    
    return render(request, 'dashboard.html', context)

# Nurse Dashboard
@login_required
@nurse_required
def nurse_dashboard(request):
    today = timezone.now().date()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'appointments_today': 0,
        'available_beds': Bed.objects.filter(status='vacant').count(),
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(
            status='admitted'
        ).count(),
        'pending_appointments': 0,
        'pending_lab_tests': 0,
        'low_stock_medicines': 0,
        'recent_appointments': IPDRecord.objects.filter(
            status='admitted'
        ).select_related('patient', 'doctor__user', 'bed__ward').order_by('-admission_date')[:5],
        'today': today,
        'user_role': 'nurse'
    }
    
    return render(request, 'dashboard.html', context)

# Pharmacist Dashboard
@login_required
@pharmacist_required
def pharmacist_dashboard(request):
    today = timezone.now().date()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'appointments_today': 0,
        'available_beds': Bed.objects.filter(status='vacant').count(),
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(status='admitted').count(),
        'pending_appointments': PharmacyPrescription.objects.filter(
            status='pending'
        ).count(),
        'pending_lab_tests': 0,
        'low_stock_medicines': Medicine.objects.filter(
            stock_quantity__lte=models.F('reorder_level')
        ).count(),
        'recent_appointments': PharmacyPrescription.objects.select_related(
            'patient', 'doctor__user'
        ).order_by('-created_at')[:5],
        'today': today,
        'user_role': 'pharmacist'
    }
    
    return render(request, 'dashboard.html', context)

# Lab Technician Dashboard
@login_required
@lab_technician_required
def lab_technician_dashboard(request):
    today = timezone.now().date()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'appointments_today': 0,
        'available_beds': Bed.objects.filter(status='vacant').count(),
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(status='admitted').count(),
        'pending_appointments': LabTestRequest.objects.filter(
            status='pending'
        ).count(),
        'pending_lab_tests': LabTestRequest.objects.filter(
            status='in_progress'
        ).count(),
        'low_stock_medicines': 0,
        'recent_appointments': LabTestRequest.objects.select_related(
            'patient', 'doctor__user', 'test'
        ).order_by('-requested_date')[:5],
        'today': today,
        'user_role': 'lab_technician'
    }
    
    return render(request, 'dashboard.html', context)

# Patient Dashboard
@login_required
@patient_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None
    
    today = timezone.now().date()
    
    context = {
        'patient': patient,
        'total_patients': 1,
        'total_doctors': Doctor.objects.count(),
        'appointments_today': Appointment.objects.filter(
            patient=patient,
            appointment_date=today
        ).count() if patient else 0,
        'available_beds': 0,
        'today_revenue': 0,
        'monthly_revenue': 0,
        'ipd_patients': IPDRecord.objects.filter(
            patient=patient,
            status='admitted'
        ).count() if patient else 0,
        'pending_appointments': Appointment.objects.filter(
            patient=patient,
            status='pending'
        ).count() if patient else 0,
        'pending_lab_tests': 0,
        'low_stock_medicines': 0,
        'recent_appointments': Appointment.objects.filter(
            patient=patient
        ).select_related('doctor__user').order_by('-appointment_date')[:5] if patient else [],
        'today': today,
        'user_role': 'patient'
    }
    
    return render(request, 'dashboard.html', context)

# Patient Management Views
@login_required
@role_required('admin', 'receptionist', 'doctor', 'nurse')
def patient_list(request):
    patients = Patient.objects.all().order_by('-registered_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            Q(patient_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    context = {
        'patients': patients,
        'search_query': search_query
    }
    return render(request, 'patients/patient_list.html', context)

@login_required
@role_required('admin', 'receptionist')
def patient_add(request):
    if request.method == 'POST':
        # Generate unique patient ID
        patient_id = generate_unique_id('PAT')
        
        patient = Patient.objects.create(
            patient_id=patient_id,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            blood_group=request.POST.get('blood_group'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
            address=request.POST.get('address'),
            emergency_contact=request.POST.get('emergency_contact'),
            emergency_contact_name=request.POST.get('emergency_contact_name'),
            medical_history=request.POST.get('medical_history', ''),
            allergies=request.POST.get('allergies', '')
        )
        
        messages.success(request, f'Patient {patient.get_full_name()} added successfully!')
        return redirect('patient_list')
    
    return render(request, 'patients/patient_form.html')

@login_required
@role_required('admin', 'receptionist', 'doctor')
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.gender = request.POST.get('gender')
        patient.date_of_birth = request.POST.get('date_of_birth')
        patient.blood_group = request.POST.get('blood_group')
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email', '')
        patient.address = request.POST.get('address')
        patient.emergency_contact = request.POST.get('emergency_contact')
        patient.emergency_contact_name = request.POST.get('emergency_contact_name')
        patient.medical_history = request.POST.get('medical_history', '')
        patient.allergies = request.POST.get('allergies', '')
        patient.save()
        
        messages.success(request, f'Patient {patient.get_full_name()} updated successfully!')
        return redirect('patient_detail', pk=pk)
    
    context = {'patient': patient, 'edit_mode': True}
    return render(request, 'patients/patient_form.html', context)

@login_required
@role_required('admin', 'receptionist', 'doctor', 'nurse')
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    context = {
        'patient': patient,
        'appointments': patient.appointments.all().order_by('-appointment_date')[:10],
        'opd_records': patient.opd_records.all().order_by('-visit_date')[:10],
        'ipd_records': patient.ipd_records.all().order_by('-admission_date')[:10],
        'medical_reports': patient.medical_reports.all().order_by('-uploaded_date')[:10],
        'bills': Bill.objects.filter(patient=patient).order_by('-created_at')[:10]
    }
    return render(request, 'patients/patient_detail.html', context)

@login_required
@admin_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient_name = patient.get_full_name()
    patient.delete()
    messages.success(request, f'Patient {patient_name} deleted successfully!')
    return redirect('patient_list')

# Doctor Management Views
@login_required
@role_required('admin', 'receptionist')
def doctor_list(request):
    doctors = Doctor.objects.select_related('user').all()
    context = {'doctors': doctors}
    return render(request, 'doctors/doctor_list.html', context)

@login_required
@admin_required
def doctor_add(request):
    if request.method == 'POST':
        # Create user account
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            role='doctor',
            phone=request.POST.get('phone'),
            address=request.POST.get('address', '')
        )
        
        # Create doctor profile
        Doctor.objects.create(
            user=user,
            specialization=request.POST.get('specialization'),
            qualification=request.POST.get('qualification'),
            experience_years=request.POST.get('experience_years', 0),
            consultation_fee=request.POST.get('consultation_fee', 0),
            available_days=request.POST.get('available_days'),
            available_time_start=request.POST.get('available_time_start'),
            available_time_end=request.POST.get('available_time_end')
        )
        
        messages.success(request, f'Dr. {user.get_full_name()} added successfully!')
        return redirect('doctor_list')
    
    return render(request, 'doctors/doctor_form.html')

@login_required
@admin_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        doctor.user.first_name = request.POST.get('first_name')
        doctor.user.last_name = request.POST.get('last_name')
        doctor.user.email = request.POST.get('email')
        doctor.user.save()
        
        doctor.specialization = request.POST.get('specialization')
        doctor.qualification = request.POST.get('qualification')
        doctor.experience_years = request.POST.get('experience_years', 0)
        doctor.consultation_fee = request.POST.get('consultation_fee', 0)
        doctor.available_days = request.POST.get('available_days')
        doctor.available_time_start = request.POST.get('available_time_start')
        doctor.available_time_end = request.POST.get('available_time_end')
        doctor.is_available = request.POST.get('is_available') == 'on'
        doctor.save()
        
        messages.success(request, f'Dr. {doctor.user.get_full_name()} updated successfully!')
        return redirect('doctor_list')
    
    context = {'doctor': doctor, 'edit_mode': True}
    return render(request, 'doctors/doctor_form.html', context)

# Appointment Management Views
@login_required
@role_required('admin', 'receptionist', 'doctor')
def appointment_list(request):
    appointments = Appointment.objects.select_related(
        'patient', 'doctor__user'
    ).all().order_by('-appointment_date', '-appointment_time')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter
    }
    return render(request, 'appointments/appointment_list.html', context)

@login_required
@role_required('admin', 'receptionist')
def appointment_add(request):
    if request.method == 'POST':
        appointment_number = generate_unique_id('APT')
        
        appointment = Appointment.objects.create(
            appointment_number=appointment_number,
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            appointment_date=request.POST.get('appointment_date'),
            appointment_time=request.POST.get('appointment_time'),
            reason=request.POST.get('reason'),
            status='pending',
            created_by=request.user
        )
        
        messages.success(request, f'Appointment {appointment_number} created successfully!')
        return redirect('appointment_list')
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.filter(is_available=True)
    }
    return render(request, 'appointments/appointment_form.html', context)

@login_required
@role_required('admin', 'receptionist', 'doctor')
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.patient_id = request.POST.get('patient')
        appointment.doctor_id = request.POST.get('doctor')
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.appointment_time = request.POST.get('appointment_time')
        appointment.reason = request.POST.get('reason')
        appointment.status = request.POST.get('status')
        appointment.notes = request.POST.get('notes', '')
        appointment.save()
        
        messages.success(request, f'Appointment {appointment.appointment_number} updated successfully!')
        return redirect('appointment_list')
    
    context = {
        'appointment': appointment,
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'edit_mode': True
    }
    return render(request, 'appointments/appointment_form.html', context)

@login_required
@role_required('admin', 'receptionist', 'doctor')
def appointment_approve(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'approved'
    appointment.save()
    messages.success(request, f'Appointment {appointment.appointment_number} approved!')
    return redirect('appointment_list')

@login_required
@role_required('admin', 'receptionist', 'doctor')
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, f'Appointment {appointment.appointment_number} cancelled!')
    return redirect('appointment_list')

# OPD Management Views
@login_required
@role_required('admin', 'doctor')
def opd_list(request):
    opd_records = OPDRecord.objects.select_related(
        'patient', 'doctor__user'
    ).all().order_by('-visit_date')
    
    context = {'opd_records': opd_records}
    return render(request, 'opd/opd_list.html', context)

@login_required
@doctor_required
def opd_add(request):
    if request.method == 'POST':
        opd_number = generate_unique_id('OPD')
        
        opd_record = OPDRecord.objects.create(
            opd_number=opd_number,
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            symptoms=request.POST.get('symptoms'),
            diagnosis=request.POST.get('diagnosis'),
            prescription=request.POST.get('prescription'),
            vitals_bp=request.POST.get('vitals_bp', ''),
            vitals_temperature=request.POST.get('vitals_temperature', ''),
            vitals_pulse=request.POST.get('vitals_pulse', ''),
            vitals_weight=request.POST.get('vitals_weight', ''),
            notes=request.POST.get('notes', '')
        )
        
        messages.success(request, f'OPD Record {opd_number} created successfully!')
        return redirect('opd_list')
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all()
    }
    return render(request, 'opd/opd_form.html', context)

@login_required
@role_required('admin', 'doctor')
def opd_detail(request, pk):
    opd_record = get_object_or_404(OPDRecord, pk=pk)
    context = {'opd_record': opd_record}
    return render(request, 'opd/opd_detail.html', context)

# IPD Management Views
@login_required
@role_required('admin', 'doctor', 'nurse')
def ipd_list(request):
    ipd_records = IPDRecord.objects.select_related(
        'patient', 'doctor__user', 'bed__ward'
    ).all().order_by('-admission_date')
    
    context = {'ipd_records': ipd_records}
    return render(request, 'ipd/ipd_list.html', context)

@login_required
@role_required('admin', 'doctor')
def ipd_add(request):
    if request.method == 'POST':
        ipd_number = generate_unique_id('IPD')
        bed_id = request.POST.get('bed')
        
        # Update bed status
        bed = Bed.objects.get(pk=bed_id)
        bed.status = 'occupied'
        bed.save()
        
        ipd_record = IPDRecord.objects.create(
            ipd_number=ipd_number,
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            bed=bed,
            admission_date=request.POST.get('admission_date'),
            diagnosis=request.POST.get('diagnosis'),
            treatment_notes=request.POST.get('treatment_notes', ''),
            status='admitted'
        )
        
        messages.success(request, f'Patient admitted with IPD Number {ipd_number}!')
        return redirect('ipd_list')
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'available_beds': Bed.objects.filter(status='vacant').select_related('ward')
    }
    return render(request, 'ipd/ipd_form.html', context)

@login_required
@role_required('admin', 'doctor', 'nurse')
def ipd_discharge(request, pk):
    ipd_record = get_object_or_404(IPDRecord, pk=pk)
    
    if request.method == 'POST':
        ipd_record.discharge_date = timezone.now()
        ipd_record.status = 'discharged'
        ipd_record.save()
        
        # Update bed status
        if ipd_record.bed:
            ipd_record.bed.status = 'vacant'
            ipd_record.bed.save()
        
        messages.success(request, f'Patient discharged from IPD {ipd_record.ipd_number}!')
        return redirect('ipd_list')
    
    context = {'ipd_record': ipd_record}
    return render(request, 'ipd/ipd_discharge.html', context)

# Ward and Bed Management Views
@login_required
@admin_required
def ward_list(request):
    wards = Ward.objects.all()
    context = {'wards': wards}
    return render(request, 'wards/ward_list.html', context)

@login_required
@admin_required
def ward_add(request):
    if request.method == 'POST':
        ward = Ward.objects.create(
            ward_name=request.POST.get('ward_name'),
            ward_type=request.POST.get('ward_type'),
            floor=request.POST.get('floor'),
            total_beds=request.POST.get('total_beds'),
            charge_per_day=request.POST.get('charge_per_day')
        )
        
        # Create beds for the ward
        total_beds = int(request.POST.get('total_beds'))
        for i in range(1, total_beds + 1):
            Bed.objects.create(
                ward=ward,
                bed_number=str(i),
                status='vacant'
            )
        
        messages.success(request, f'Ward {ward.ward_name} created with {total_beds} beds!')
        return redirect('ward_list')
    
    return render(request, 'wards/ward_form.html')

@login_required
@admin_required
def bed_list(request):
    beds = Bed.objects.select_related('ward').all()
    
    # Filter by ward
    ward_filter = request.GET.get('ward', '')
    if ward_filter:
        beds = beds.filter(ward_id=ward_filter)
    
    context = {
        'beds': beds,
        'wards': Ward.objects.all(),
        'ward_filter': ward_filter
    }
    return render(request, 'wards/bed_list.html', context)

# Pharmacy Management Views
@login_required
@role_required('admin', 'pharmacist')
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('medicine_name')
    
    # Filter expired and low stock
    show_expired = request.GET.get('expired', '')
    show_low_stock = request.GET.get('low_stock', '')
    
    if show_expired:
        medicines = medicines.filter(expiry_date__lt=timezone.now().date())
    if show_low_stock:
        medicines = medicines.filter(stock_quantity__lte=models.F('reorder_level'))
    
    context = {
        'medicines': medicines,
        'show_expired': show_expired,
        'show_low_stock': show_low_stock
    }
    return render(request, 'pharmacy/medicine_list.html', context)

@login_required
@pharmacist_required
def medicine_add(request):
    if request.method == 'POST':
        medicine = Medicine.objects.create(
            medicine_name=request.POST.get('medicine_name'),
            medicine_type=request.POST.get('medicine_type'),
            manufacturer=request.POST.get('manufacturer'),
            description=request.POST.get('description', ''),
            unit_price=request.POST.get('unit_price'),
            stock_quantity=request.POST.get('stock_quantity', 0),
            reorder_level=request.POST.get('reorder_level', 10),
            expiry_date=request.POST.get('expiry_date')
        )
        
        messages.success(request, f'Medicine {medicine.medicine_name} added successfully!')
        return redirect('medicine_list')
    
    return render(request, 'pharmacy/medicine_form.html')

@login_required
@pharmacist_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        medicine.medicine_name = request.POST.get('medicine_name')
        medicine.medicine_type = request.POST.get('medicine_type')
        medicine.manufacturer = request.POST.get('manufacturer')
        medicine.description = request.POST.get('description', '')
        medicine.unit_price = request.POST.get('unit_price')
        medicine.stock_quantity = request.POST.get('stock_quantity')
        medicine.reorder_level = request.POST.get('reorder_level')
        medicine.expiry_date = request.POST.get('expiry_date')
        medicine.save()
        
        messages.success(request, f'Medicine {medicine.medicine_name} updated successfully!')
        return redirect('medicine_list')
    
    context = {'medicine': medicine, 'edit_mode': True}
    return render(request, 'pharmacy/medicine_form.html', context)

# Laboratory Management Views
@login_required
@admin_required
def lab_test_list(request):
    lab_tests = LabTest.objects.all().order_by('test_name')
    context = {'lab_tests': lab_tests}
    return render(request, 'laboratory/lab_test_list.html', context)

@login_required
@admin_required
def lab_test_add(request):
    if request.method == 'POST':
        lab_test = LabTest.objects.create(
            test_name=request.POST.get('test_name'),
            test_code=request.POST.get('test_code'),
            description=request.POST.get('description', ''),
            normal_range=request.POST.get('normal_range', ''),
            price=request.POST.get('price')
        )
        
        messages.success(request, f'Lab Test {lab_test.test_name} added successfully!')
        return redirect('lab_test_list')
    
    return render(request, 'laboratory/lab_test_form.html')

@login_required
@role_required('admin', 'doctor', 'lab_technician')
def lab_request_list(request):
    lab_requests = LabTestRequest.objects.select_related(
        'patient', 'doctor__user', 'test'
    ).all().order_by('-requested_date')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        lab_requests = lab_requests.filter(status=status_filter)
    
    context = {
        'lab_requests': lab_requests,
        'status_filter': status_filter
    }
    return render(request, 'laboratory/lab_request_list.html', context)

@login_required
@doctor_required
def lab_request_add(request):
    if request.method == 'POST':
        request_number = generate_unique_id('LAB')
        
        lab_request = LabTestRequest.objects.create(
            request_number=request_number,
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            test_id=request.POST.get('test'),
            status='pending'
        )
        
        messages.success(request, f'Lab Test Request {request_number} created successfully!')
        return redirect('lab_request_list')
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'lab_tests': LabTest.objects.all()
    }
    return render(request, 'laboratory/lab_request_form.html', context)

@login_required
@lab_technician_required
def lab_request_update(request, pk):
    lab_request = get_object_or_404(LabTestRequest, pk=pk)
    
    if request.method == 'POST':
        lab_request.status = request.POST.get('status')
        lab_request.result = request.POST.get('result', '')
        lab_request.notes = request.POST.get('notes', '')
        
        if request.FILES.get('report_file'):
            lab_request.report_file = request.FILES['report_file']
        
        if lab_request.status == 'completed':
            lab_request.completed_date = timezone.now()
            lab_request.technician = request.user
        
        lab_request.save()
        
        messages.success(request, f'Lab Request {lab_request.request_number} updated successfully!')
        return redirect('lab_request_list')
    
    context = {'lab_request': lab_request}
    return render(request, 'laboratory/lab_request_update.html', context)

# Billing Management Views
@login_required
@admin_required
def bill_list(request):
    bills = Bill.objects.select_related('patient').all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    context = {
        'bills': bills,
        'status_filter': status_filter
    }
    return render(request, 'billing/bill_list.html', context)

@login_required
@admin_required
def bill_add(request):
    if request.method == 'POST':
        bill_number = generate_unique_id('BILL')
        
        # Convert string values to Decimal
        consultation_fee = Decimal(request.POST.get('consultation_fee', 0) or 0)
        room_charges = Decimal(request.POST.get('room_charges', 0) or 0)
        medicine_charges = Decimal(request.POST.get('medicine_charges', 0) or 0)
        lab_charges = Decimal(request.POST.get('lab_charges', 0) or 0)
        other_charges = Decimal(request.POST.get('other_charges', 0) or 0)
        discount = Decimal(request.POST.get('discount', 0) or 0)
        tax = Decimal(request.POST.get('tax', 0) or 0)
        
        bill = Bill.objects.create(
            bill_number=bill_number,
            patient_id=request.POST.get('patient'),
            consultation_fee=consultation_fee,
            room_charges=room_charges,
            medicine_charges=medicine_charges,
            lab_charges=lab_charges,
            other_charges=other_charges,
            discount=discount,
            tax=tax,
            payment_method=request.POST.get('payment_method', ''),
            created_by=request.user
        )
        
        messages.success(request, f'Bill {bill_number} created successfully!')
        return redirect('bill_detail', pk=bill.pk)
    
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all()
    }
    return render(request, 'billing/bill_form.html', context)

@login_required
@admin_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    context = {'bill': bill}
    return render(request, 'billing/bill_detail.html', context)

@login_required
@admin_required
def bill_payment(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        bill.amount_paid += amount
        bill.payment_method = request.POST.get('payment_method')
        bill.save()
        
        messages.success(request, f'Payment of ₹{amount} recorded successfully!')
        return redirect('bill_detail', pk=pk)
    
    context = {'bill': bill}
    return render(request, 'billing/bill_payment.html', context)

# Staff Management Views
@login_required
@admin_required
def staff_list(request):
    staff = User.objects.filter(profile__isnull=False).select_related('profile')
    context = {'staff': staff}
    return render(request, 'staff/staff_list.html', context)

@login_required
@admin_required
def staff_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        UserProfile.objects.create(
            user=user,
            role=request.POST.get('role'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address', ''),
            date_of_birth=request.POST.get('date_of_birth') or None
        )
        
        messages.success(request, f'Staff {user.get_full_name()} added successfully!')
        return redirect('staff_list')
    
    return render(request, 'staff/staff_form.html')

@login_required
@admin_required
def attendance_list(request):
    today = timezone.now().date()
    attendances = Attendance.objects.filter(date=today).select_related('user')
    
    # Date filter
    date_filter = request.GET.get('date', '')
    if date_filter:
        attendances = Attendance.objects.filter(date=date_filter).select_related('user')
    
    context = {
        'attendances': attendances,
        'date_filter': date_filter or today
    }
    return render(request, 'staff/attendance_list.html', context)

@login_required
@admin_required
def attendance_mark(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        attendance, created = Attendance.objects.update_or_create(
            user_id=user_id,
            date=date,
            defaults={
                'status': status,
                'check_in_time': request.POST.get('check_in_time') or None,
                'check_out_time': request.POST.get('check_out_time') or None,
                'notes': request.POST.get('notes', '')
            }
        )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_list')
    
    context = {
        'staff': User.objects.filter(profile__isnull=False),
        'today': timezone.now().date()
    }
    return render(request, 'staff/attendance_form.html', context)

# Reports and Analytics Views
@login_required
@admin_required
def reports_dashboard(request):
    today = timezone.now().date()
    first_day_month = today.replace(day=1)
    
    context = {
        # Daily stats
        'daily_patients': Patient.objects.filter(registered_date__date=today).count(),
        'daily_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'daily_revenue': Bill.objects.filter(created_at__date=today).aggregate(
            total=Sum('total_amount'))['total'] or 0,
        
        # Monthly stats
        'monthly_patients': Patient.objects.filter(
            registered_date__date__gte=first_day_month).count(),
        'monthly_appointments': Appointment.objects.filter(
            appointment_date__gte=first_day_month).count(),
        'monthly_revenue': Bill.objects.filter(
            created_at__date__gte=first_day_month).aggregate(
            total=Sum('total_amount'))['total'] or 0,
        
        # Department wise
        'opd_count': OPDRecord.objects.filter(visit_date__date=today).count(),
        'ipd_count': IPDRecord.objects.filter(status='admitted').count(),
        'lab_tests_today': LabTestRequest.objects.filter(requested_date__date=today).count(),
        
        # Top doctors
        'top_doctors': Doctor.objects.annotate(
            appointment_count=Count('appointments')
        ).order_by('-appointment_count')[:5]
    }
    
    return render(request, 'reports/reports_dashboard.html', context)

# Profile Management
@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except:
        profile = None
    
    context = {'profile': profile}
    return render(request, 'profile.html', context)

@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except:
        profile = UserProfile.objects.create(user=request.user, role='admin')
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address', '')
        
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')
    
    context = {'profile': profile}
    return render(request, 'profile_edit.html', context)

# Error Pages
def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
