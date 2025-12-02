# Role-Based Access Control Implementation Guide

## Overview
This document outlines the complete role-based access control (RBAC) system implemented in the Hospital Management System (HMS). The system ensures strict separation of concerns between 7 user roles with completely different functionalities and permissions.

## Roles and Their Permissions

### 1. Admin
**Access Level:** Full System Access
**Functionalities:**
- Manage all users (create, edit, delete)
- Manage doctors (add, edit, view)
- Manage patients (add, edit, delete, view)
- Manage appointments (create, edit, approve, cancel)
- Manage wards and beds
- Manage pharmacy stock
- Manage lab tests
- View all reports and analytics
- Manage staff and attendance
- View revenue and billing reports
- Full CRUD operations on all modules

**Restricted From:**
- Cannot access doctor-specific features (OPD/IPD patient management)
- Cannot dispense medicines
- Cannot update lab results
- Cannot view patient-only features

**Dashboard:** Admin Dashboard with system-wide statistics

### 2. Doctor
**Access Level:** Patient Care & Treatment
**Functionalities:**
- View assigned appointments
- View patient list and details
- Create and manage OPD records
- Create and manage IPD records
- Write prescriptions
- Update treatment notes
- Request lab tests
- View lab results
- View patient medical history

**Restricted From:**
- Cannot manage other doctors
- Cannot manage staff
- Cannot access billing
- Cannot manage pharmacy stock
- Cannot manage wards/beds
- Cannot access admin features
- Cannot view revenue reports

**Dashboard:** Doctor Dashboard showing appointments, patients, and pending tasks

### 3. Receptionist
**Access Level:** Appointment & Patient Registration
**Functionalities:**
- Book appointments
- Register new patients
- View patient list
- View doctor list
- Manage appointment status
- View appointment list

**Restricted From:**
- Cannot access medical records
- Cannot manage doctors
- Cannot access pharmacy
- Cannot access lab
- Cannot access billing
- Cannot access staff management
- Cannot access admin features

**Dashboard:** Receptionist Dashboard showing appointments and patient registrations

### 4. Nurse
**Access Level:** Patient Care & Vitals
**Functionalities:**
- View admitted patients (IPD)
- Update patient vitals
- View patient details
- View patient medical history
- Manage IPD records
- Discharge patients

**Restricted From:**
- Cannot book appointments
- Cannot manage pharmacy
- Cannot access lab
- Cannot access billing
- Cannot manage doctors
- Cannot access admin features

**Dashboard:** Nurse Dashboard showing admitted patients and vitals

### 5. Pharmacist
**Access Level:** Medicine Management
**Functionalities:**
- View medicine stock
- Add new medicines
- Edit medicine details
- Manage medicine expiry
- Track low stock medicines
- Dispense medicines
- View prescriptions

**Restricted From:**
- Cannot access patient records
- Cannot manage appointments
- Cannot access lab
- Cannot access billing
- Cannot manage doctors
- Cannot access admin features

**Dashboard:** Pharmacist Dashboard showing stock levels and pending prescriptions

### 6. Lab Technician
**Access Level:** Lab Test Management
**Functionalities:**
- View lab test requests
- Update test status
- Upload lab reports
- Enter test results
- View patient details for tests

**Restricted From:**
- Cannot request tests (only doctors can)
- Cannot manage pharmacy
- Cannot access appointments
- Cannot manage patients
- Cannot access billing
- Cannot access admin features

**Dashboard:** Lab Technician Dashboard showing pending and in-progress tests

### 7. Patient
**Access Level:** Personal Health Records
**Functionalities:**
- View own profile
- View own appointments
- View own medical reports
- View own bills
- View own medical history

**Restricted From:**
- Cannot access other patient records
- Cannot manage appointments (receptionist does)
- Cannot access staff features
- Cannot access admin features
- Cannot access pharmacy/lab management

**Dashboard:** Patient Dashboard showing personal health information

## Implementation Details

### 1. Decorators (core/decorators.py)
Created role-based decorators for view protection:

```python
@admin_required          # Admin only
@doctor_required         # Doctor only
@receptionist_required   # Receptionist only
@nurse_required          # Nurse only
@pharmacist_required     # Pharmacist only
@lab_technician_required # Lab Technician only
@patient_required        # Patient only
@role_required(*roles)   # Multiple roles allowed
```

**Usage Example:**
```python
@login_required
@admin_required
def staff_list(request):
    # Only admins can access this view
    pass

@login_required
@role_required('admin', 'receptionist')
def patient_list(request):
    # Both admins and receptionists can access
    pass
```

### 2. Views (core/views.py)
All views have been updated with appropriate role decorators:

**Admin-Only Views:**
- `admin_dashboard` - System overview
- `doctor_add`, `doctor_edit` - Doctor management
- `ward_list`, `ward_add` - Ward management
- `bed_list` - Bed management
- `lab_test_list`, `lab_test_add` - Lab test setup
- `bill_list`, `bill_add`, `bill_detail`, `bill_payment` - Billing
- `staff_list`, `staff_add` - Staff management
- `attendance_list`, `attendance_mark` - Attendance
- `reports_dashboard` - Analytics
- `patient_delete` - Patient deletion

**Doctor-Only Views:**
- `doctor_dashboard` - Doctor overview
- `opd_add` - Create OPD records
- `lab_request_add` - Request lab tests

**Receptionist-Only Views:**
- `receptionist_dashboard` - Receptionist overview
- `patient_add` - Register patients
- `appointment_add` - Book appointments

**Nurse-Only Views:**
- `nurse_dashboard` - Nurse overview

**Pharmacist-Only Views:**
- `pharmacist_dashboard` - Pharmacist overview
- `medicine_add`, `medicine_edit` - Manage medicines

**Lab Technician-Only Views:**
- `lab_technician_dashboard` - Lab overview
- `lab_request_update` - Update test results

**Patient-Only Views:**
- `patient_dashboard` - Patient overview

**Multi-Role Views:**
- `patient_list` - Admin, Receptionist, Doctor, Nurse
- `patient_detail` - Admin, Receptionist, Doctor, Nurse
- `patient_edit` - Admin, Receptionist, Doctor
- `doctor_list` - Admin, Receptionist
- `appointment_list` - Admin, Receptionist, Doctor
- `appointment_edit` - Admin, Receptionist, Doctor
- `appointment_approve` - Admin, Receptionist, Doctor
- `appointment_cancel` - Admin, Receptionist, Doctor
- `opd_list` - Admin, Doctor
- `opd_detail` - Admin, Doctor
- `ipd_list` - Admin, Doctor, Nurse
- `ipd_add` - Admin, Doctor
- `ipd_discharge` - Admin, Doctor, Nurse
- `medicine_list` - Admin, Pharmacist
- `lab_request_list` - Admin, Doctor, Lab Technician

### 3. Login Redirect (core/views.py)
The login view now redirects users to their role-specific dashboard:

```python
def login_view(request):
    # ... authentication code ...
    if user is not None:
        login(request, user)
        
        # Role-based redirect
        role = user.profile.role
        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'doctor':
            return redirect('doctor_dashboard')
        # ... etc for other roles
```

### 4. URLs (core/urls.py)
Added role-specific dashboard routes:

```python
path('dashboard/', views.dashboard, name='dashboard'),  # Redirects to role dashboard
path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
path('dashboard/nurse/', views.nurse_dashboard, name='nurse_dashboard'),
path('dashboard/pharmacist/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
path('dashboard/lab-technician/', views.lab_technician_dashboard, name='lab_technician_dashboard'),
path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
```

### 5. Templates (templates/base.html)
The sidebar navigation is now role-aware and shows only relevant menu items:

```html
<!-- Admin Only -->
{% if user.profile.role == 'admin' %}
    <a class="nav-link" href="{% url 'patient_list' %}">Patients</a>
    <a class="nav-link" href="{% url 'doctor_list' %}">Doctors</a>
    <!-- ... all admin features ... -->
{% endif %}

<!-- Doctor Only -->
{% if user.profile.role == 'doctor' %}
    <a class="nav-link" href="{% url 'appointment_list' %}">Appointments</a>
    <a class="nav-link" href="{% url 'opd_list' %}">OPD</a>
    <!-- ... doctor features ... -->
{% endif %}

<!-- Similar for other roles -->
```

### 6. Models (core/models.py)
Updated Patient model to support patient users:

```python
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                related_name='patient_profile', 
                                null=True, blank=True)
    # ... other fields ...
```

## Security Features

### 1. Decorator-Based Access Control
- Every view is protected with role decorators
- Unauthorized access attempts redirect to dashboard with error message
- No cross-role access possible

### 2. Template-Level Filtering
- Menu items only show for authorized roles
- Prevents UI confusion and accidental navigation attempts

### 3. Database-Level Separation
- Each role has specific data access patterns
- Doctors only see their appointments
- Patients only see their records

### 4. Error Handling
- Graceful error messages for unauthorized access
- Automatic redirects to appropriate dashboard
- Session validation on every request

## Access Control Matrix

| Feature | Admin | Doctor | Receptionist | Nurse | Pharmacist | Lab Tech | Patient |
|---------|-------|--------|--------------|-------|------------|----------|---------|
| Dashboard | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Patients (CRUD) | ✓ | R | C/R | R | ✗ | ✗ | Own |
| Doctors (CRUD) | ✓ | ✗ | R | ✗ | ✗ | ✗ | ✗ |
| Appointments | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | Own |
| OPD | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| IPD | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Wards/Beds | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Pharmacy | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Lab | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Billing | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | Own |
| Staff | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Reports | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

Legend: ✓ = Full Access, R = Read Only, C = Create, Own = Own Records Only, ✗ = No Access

## Testing the Implementation

### 1. Test Admin Access
- Login as admin user
- Verify all menu items visible
- Try accessing doctor-only features (should redirect)

### 2. Test Doctor Access
- Login as doctor user
- Verify only doctor menu items visible
- Try accessing admin features (should redirect)
- Verify can only see own appointments

### 3. Test Receptionist Access
- Login as receptionist user
- Verify appointment and patient registration features
- Try accessing pharmacy (should redirect)

### 4. Test Nurse Access
- Login as nurse user
- Verify only IPD features visible
- Try accessing OPD (should redirect)

### 5. Test Pharmacist Access
- Login as pharmacist user
- Verify only pharmacy features visible
- Try accessing appointments (should redirect)

### 6. Test Lab Technician Access
- Login as lab technician user
- Verify only lab request features visible
- Try accessing patient management (should redirect)

### 7. Test Patient Access
- Login as patient user
- Verify only personal dashboard visible
- Try accessing admin features (should redirect)

## Migration Notes

If you have existing users without profiles:
1. Create UserProfile for each user with appropriate role
2. For patient users, create Patient record with user link
3. Test access after migration

## Future Enhancements

1. **Permission Groups:** Use Django's built-in permission system for finer control
2. **Audit Logging:** Track all access attempts and modifications
3. **Time-Based Access:** Restrict access based on shift timings
4. **Department-Based Access:** Limit doctor access to specific departments
5. **API Permissions:** Extend RBAC to REST API endpoints

## Troubleshooting

### Issue: User sees blank sidebar
**Solution:** Ensure user has a UserProfile with valid role

### Issue: Redirect loop
**Solution:** Check that user's role matches one of the allowed roles in decorator

### Issue: Menu items not showing
**Solution:** Verify user.profile.role matches the template condition

### Issue: Access denied on valid action
**Solution:** Check view decorator and ensure user role is in allowed list

## Files Modified

1. `core/decorators.py` - NEW: Role-based decorators
2. `core/views.py` - Updated: All views with role decorators and role-specific dashboards
3. `core/urls.py` - Updated: Added role-specific dashboard routes
4. `core/models.py` - Updated: Patient model with user link
5. `templates/base.html` - Updated: Role-based sidebar navigation

## Conclusion

The HMS now has a complete role-based access control system ensuring:
- ✓ Complete role separation
- ✓ No cross-role access
- ✓ Intuitive role-specific dashboards
- ✓ Secure decorator-based protection
- ✓ Template-level filtering
- ✓ Graceful error handling
- ✓ Maintains existing design and colors
