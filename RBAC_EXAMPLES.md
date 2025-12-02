# Role-Based Access Control - Usage Examples

## Example 1: Creating an Admin-Only View

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import admin_required

@login_required
@admin_required
def system_settings(request):
    """Only admins can access system settings"""
    context = {
        'total_users': User.objects.count(),
        'total_patients': Patient.objects.count(),
        'system_status': 'Operational'
    }
    return render(request, 'admin/settings.html', context)
```

## Example 2: Creating a Multi-Role View

```python
from core.decorators import role_required

@login_required
@role_required('admin', 'receptionist', 'doctor')
def view_appointments(request):
    """Admins, receptionists, and doctors can view appointments"""
    appointments = Appointment.objects.all()
    context = {'appointments': appointments}
    return render(request, 'appointments/list.html', context)
```

## Example 3: Role-Specific Logic in View

```python
@login_required
def dashboard(request):
    """Redirect to role-specific dashboard"""
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
    
    return redirect('login')
```

## Example 4: Doctor-Specific Dashboard

```python
@login_required
@doctor_required
def doctor_dashboard(request):
    """Doctor dashboard showing appointments and patients"""
    try:
        doctor = request.user.doctor
    except:
        messages.error(request, 'Doctor profile not found.')
        return redirect('logout')
    
    today = timezone.now().date()
    
    context = {
        'doctor': doctor,
        'appointments_today': Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            doctor=doctor,
            status='pending'
        ).count(),
        'my_appointments': Appointment.objects.filter(
            doctor=doctor
        ).select_related('patient').order_by('-appointment_date')[:10],
        'my_patients': Patient.objects.filter(
            appointments__doctor=doctor
        ).distinct().count(),
        'user_role': 'doctor'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 5: Receptionist-Specific Dashboard

```python
@login_required
@receptionist_required
def receptionist_dashboard(request):
    """Receptionist dashboard for appointments and patient registration"""
    today = timezone.now().date()
    
    context = {
        'appointments_today': Appointment.objects.filter(
            appointment_date=today
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            status='pending'
        ).count(),
        'recent_appointments': Appointment.objects.select_related(
            'patient', 'doctor__user'
        ).order_by('-created_at')[:10],
        'total_patients': Patient.objects.count(),
        'user_role': 'receptionist'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 6: Nurse-Specific Dashboard

```python
@login_required
@nurse_required
def nurse_dashboard(request):
    """Nurse dashboard showing admitted patients"""
    context = {
        'admitted_patients': IPDRecord.objects.filter(
            status='admitted'
        ).select_related('patient', 'doctor__user', 'bed__ward').count(),
        'ipd_records': IPDRecord.objects.filter(
            status='admitted'
        ).select_related('patient', 'doctor__user', 'bed__ward')[:10],
        'user_role': 'nurse'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 7: Pharmacist-Specific Dashboard

```python
@login_required
@pharmacist_required
def pharmacist_dashboard(request):
    """Pharmacist dashboard for medicine management"""
    context = {
        'pending_prescriptions': PharmacyPrescription.objects.filter(
            status='pending'
        ).count(),
        'low_stock_medicines': Medicine.objects.filter(
            stock_quantity__lte=models.F('reorder_level')
        ).count(),
        'expired_medicines': Medicine.objects.filter(
            expiry_date__lt=timezone.now().date()
        ).count(),
        'recent_prescriptions': PharmacyPrescription.objects.select_related(
            'patient', 'doctor__user'
        ).order_by('-created_at')[:10],
        'user_role': 'pharmacist'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 8: Lab Technician-Specific Dashboard

```python
@login_required
@lab_technician_required
def lab_technician_dashboard(request):
    """Lab technician dashboard for test management"""
    context = {
        'pending_tests': LabTestRequest.objects.filter(
            status='pending'
        ).count(),
        'in_progress_tests': LabTestRequest.objects.filter(
            status='in_progress'
        ).count(),
        'recent_requests': LabTestRequest.objects.select_related(
            'patient', 'doctor__user', 'test'
        ).order_by('-requested_date')[:10],
        'user_role': 'lab_technician'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 9: Patient-Specific Dashboard

```python
@login_required
@patient_required
def patient_dashboard(request):
    """Patient dashboard showing personal health records"""
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None
    
    context = {
        'patient': patient,
        'appointments': Appointment.objects.filter(
            patient=patient
        ).select_related('doctor__user').order_by('-appointment_date')[:10] if patient else [],
        'medical_reports': MedicalReport.objects.filter(
            patient=patient
        ).order_by('-uploaded_date')[:10] if patient else [],
        'bills': Bill.objects.filter(
            patient=patient
        ).order_by('-created_at')[:10] if patient else [],
        'user_role': 'patient'
    }
    
    return render(request, 'dashboard.html', context)
```

## Example 10: Template with Role-Based Menu

```html
<!-- templates/base.html -->
<div class="sidebar">
    <nav class="nav flex-column">
        <!-- Dashboard (all roles) -->
        <a class="nav-link" href="{% url 'dashboard' %}">
            <i class="fas fa-tachometer-alt"></i> Dashboard
        </a>
        
        <!-- Admin Only -->
        {% if user.profile.role == 'admin' %}
            <a class="nav-link" href="{% url 'patient_list' %}">
                <i class="fas fa-user-injured"></i> Patients
            </a>
            <a class="nav-link" href="{% url 'doctor_list' %}">
                <i class="fas fa-user-md"></i> Doctors
            </a>
            <a class="nav-link" href="{% url 'staff_list' %}">
                <i class="fas fa-users"></i> Staff
            </a>
            <a class="nav-link" href="{% url 'reports_dashboard' %}">
                <i class="fas fa-chart-bar"></i> Reports
            </a>
        {% endif %}
        
        <!-- Doctor Only -->
        {% if user.profile.role == 'doctor' %}
            <a class="nav-link" href="{% url 'appointment_list' %}">
                <i class="fas fa-calendar-check"></i> Appointments
            </a>
            <a class="nav-link" href="{% url 'opd_list' %}">
                <i class="fas fa-procedures"></i> OPD
            </a>
            <a class="nav-link" href="{% url 'ipd_list' %}">
                <i class="fas fa-bed"></i> IPD
            </a>
            <a class="nav-link" href="{% url 'lab_request_list' %}">
                <i class="fas fa-flask"></i> Lab Requests
            </a>
        {% endif %}
        
        <!-- Receptionist Only -->
        {% if user.profile.role == 'receptionist' %}
            <a class="nav-link" href="{% url 'appointment_list' %}">
                <i class="fas fa-calendar-check"></i> Appointments
            </a>
            <a class="nav-link" href="{% url 'patient_list' %}">
                <i class="fas fa-user-injured"></i> Patients
            </a>
        {% endif %}
        
        <!-- Nurse Only -->
        {% if user.profile.role == 'nurse' %}
            <a class="nav-link" href="{% url 'ipd_list' %}">
                <i class="fas fa-bed"></i> Admitted Patients
            </a>
        {% endif %}
        
        <!-- Pharmacist Only -->
        {% if user.profile.role == 'pharmacist' %}
            <a class="nav-link" href="{% url 'medicine_list' %}">
                <i class="fas fa-pills"></i> Medicines
            </a>
        {% endif %}
        
        <!-- Lab Technician Only -->
        {% if user.profile.role == 'lab_technician' %}
            <a class="nav-link" href="{% url 'lab_request_list' %}">
                <i class="fas fa-flask"></i> Lab Requests
            </a>
        {% endif %}
        
        <!-- Patient Only -->
        {% if user.profile.role == 'patient' %}
            <a class="nav-link" href="{% url 'profile_view' %}">
                <i class="fas fa-user"></i> My Profile
            </a>
        {% endif %}
    </nav>
</div>
```

## Example 11: Checking Role in View Logic

```python
@login_required
def view_patient_details(request, pk):
    """View patient details with role-based filtering"""
    patient = get_object_or_404(Patient, pk=pk)
    user_role = request.user.profile.role
    
    # Patients can only view their own records
    if user_role == 'patient':
        if patient.user != request.user:
            messages.error(request, 'You can only view your own records.')
            return redirect('patient_dashboard')
    
    # Doctors can view their patients
    elif user_role == 'doctor':
        if not patient.appointments.filter(doctor__user=request.user).exists():
            messages.error(request, 'You can only view your assigned patients.')
            return redirect('patient_list')
    
    # Nurses can view admitted patients
    elif user_role == 'nurse':
        if not patient.ipd_records.filter(status='admitted').exists():
            messages.error(request, 'Patient is not currently admitted.')
            return redirect('ipd_list')
    
    # Admins and receptionists can view all patients
    
    context = {'patient': patient}
    return render(request, 'patients/detail.html', context)
```

## Example 12: Creating a New Role-Protected Feature

```python
# Step 1: Create the view with decorator
@login_required
@role_required('admin', 'doctor')
def generate_medical_report(request, patient_id):
    """Generate medical report (admin and doctor only)"""
    patient = get_object_or_404(Patient, pk=patient_id)
    
    # Generate report logic
    report = MedicalReport.objects.create(
        patient=patient,
        report_type='discharge',
        title='Discharge Summary',
        uploaded_by=request.user
    )
    
    messages.success(request, 'Report generated successfully!')
    return redirect('patient_detail', pk=patient_id)

# Step 2: Add URL pattern
# In core/urls.py
path('patients/<int:patient_id>/report/generate/', 
     views.generate_medical_report, 
     name='generate_medical_report'),

# Step 3: Add template link (only for authorized roles)
# In templates/patients/detail.html
{% if user.profile.role in 'admin,doctor' %}
    <a href="{% url 'generate_medical_report' patient.id %}" class="btn btn-primary">
        Generate Report
    </a>
{% endif %}
```

## Example 13: Error Handling

```python
@login_required
def protected_view(request):
    """View with proper error handling"""
    try:
        user_role = request.user.profile.role
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('logout')
    
    if user_role not in ['admin', 'doctor']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # View logic here
    return render(request, 'template.html')
```

## Example 14: Testing Role Access

```python
# In Django shell or tests
from django.contrib.auth.models import User
from core.models import UserProfile

# Create test users
admin_user = User.objects.create_user('admin', 'admin@test.com', 'pass123')
UserProfile.objects.create(user=admin_user, role='admin')

doctor_user = User.objects.create_user('doctor', 'doc@test.com', 'pass123')
UserProfile.objects.create(user=doctor_user, role='doctor')

# Test access
print(admin_user.profile.role)      # Output: admin
print(doctor_user.profile.role)     # Output: doctor

# Check permissions
print(admin_user.profile.get_role_display())   # Output: Admin
print(doctor_user.profile.get_role_display())  # Output: Doctor
```

## Example 15: Extending RBAC

```python
# To add a new role:

# 1. Update UserProfile model
ROLE_CHOICES = [
    # ... existing roles ...
    ('new_role', 'New Role'),
]

# 2. Create decorator
from core.decorators import role_required

def new_role_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'new_role':
                messages.error(request, 'New Role access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

# 3. Use in views
@login_required
@new_role_required
def new_role_view(request):
    pass

# 4. Add to template
{% if user.profile.role == 'new_role' %}
    <!-- New role menu items -->
{% endif %}
```

These examples cover the most common use cases for the RBAC system. For more information, refer to the detailed documentation files.
