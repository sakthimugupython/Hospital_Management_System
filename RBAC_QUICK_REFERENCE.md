# Role-Based Access Control - Quick Reference

## How to Add Role Protection to a View

### Single Role Protection
```python
from core.decorators import admin_required

@login_required
@admin_required
def my_admin_view(request):
    # Only admins can access
    pass
```

### Multiple Roles
```python
from core.decorators import role_required

@login_required
@role_required('admin', 'receptionist')
def my_view(request):
    # Admins and receptionists can access
    pass
```

### Specific Role Decorators
```python
from core.decorators import (
    admin_required,
    doctor_required,
    receptionist_required,
    nurse_required,
    pharmacist_required,
    lab_technician_required,
    patient_required
)

@login_required
@doctor_required
def doctor_only_view(request):
    pass
```

## How to Show/Hide Menu Items

In templates, use role checks:

```html
{% if user.profile.role == 'admin' %}
    <a href="{% url 'staff_list' %}">Staff Management</a>
{% endif %}

{% if user.profile.role == 'doctor' %}
    <a href="{% url 'opd_list' %}">OPD Records</a>
{% endif %}

{% if user.profile.role in 'admin,receptionist' %}
    <a href="{% url 'appointment_list' %}">Appointments</a>
{% endif %}
```

## Role Constants

```python
ADMIN = 'admin'
DOCTOR = 'doctor'
RECEPTIONIST = 'receptionist'
NURSE = 'nurse'
PHARMACIST = 'pharmacist'
LAB_TECHNICIAN = 'lab_technician'
PATIENT = 'patient'
```

## Getting User Role

```python
# In views
user_role = request.user.profile.role

# In templates
{{ user.profile.role }}
{{ user.profile.get_role_display }}
```

## Checking Role in Views

```python
# Check single role
if request.user.profile.role == 'admin':
    # Do something

# Check multiple roles
if request.user.profile.role in ['admin', 'doctor']:
    # Do something

# Check if not a role
if request.user.profile.role != 'patient':
    # Do something
```

## Dashboard Routes

```
/dashboard/                    # Redirects to role-specific dashboard
/dashboard/admin/              # Admin dashboard
/dashboard/doctor/             # Doctor dashboard
/dashboard/receptionist/       # Receptionist dashboard
/dashboard/nurse/              # Nurse dashboard
/dashboard/pharmacist/         # Pharmacist dashboard
/dashboard/lab-technician/     # Lab technician dashboard
/dashboard/patient/            # Patient dashboard
```

## Common View Patterns

### Admin-Only Feature
```python
@login_required
@admin_required
def manage_staff(request):
    staff = User.objects.filter(profile__isnull=False)
    return render(request, 'staff/list.html', {'staff': staff})
```

### Multi-Role Feature
```python
@login_required
@role_required('admin', 'receptionist', 'doctor')
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/list.html', {'appointments': appointments})
```

### Role-Specific Logic
```python
@login_required
def dashboard(request):
    role = request.user.profile.role
    
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'doctor':
        return redirect('doctor_dashboard')
    elif role == 'receptionist':
        return redirect('receptionist_dashboard')
    # ... etc
```

## Error Handling

When a user without permission tries to access a view:
1. Decorator checks user role
2. If not authorized, redirects to dashboard
3. Error message displayed: "You do not have permission to access this page."

## Testing Access

```python
# In Django shell
from django.contrib.auth.models import User
from core.models import UserProfile

# Create test user
user = User.objects.create_user('testdoc', 'doc@test.com', 'pass123')
UserProfile.objects.create(user=user, role='doctor')

# Check role
print(user.profile.role)  # Output: doctor
```

## URL Patterns

All views follow this pattern:
```
/module/                       # List view
/module/add/                   # Add/Create view
/module/<id>/                  # Detail view
/module/<id>/edit/             # Edit view
/module/<id>/delete/           # Delete view
/module/<id>/action/           # Custom action
```

## Sidebar Navigation

The sidebar in `templates/base.html` automatically shows/hides items based on role:

```html
<!-- Automatically filtered by role -->
{% if user.profile.role == 'admin' %}
    <!-- Admin menu items -->
{% endif %}

{% if user.profile.role == 'doctor' %}
    <!-- Doctor menu items -->
{% endif %}
```

## Best Practices

1. **Always use decorators** - Never rely on template-only filtering
2. **Use role_required for multiple roles** - More readable than multiple decorators
3. **Check role in templates** - Prevent UI confusion
4. **Log access attempts** - For security auditing
5. **Test all role combinations** - Ensure no cross-access
6. **Use meaningful role names** - Keep them consistent
7. **Document role permissions** - In code comments
8. **Validate on both sides** - Backend (decorators) and frontend (templates)

## Common Mistakes to Avoid

❌ **Wrong:** Only checking role in template
```python
# BAD - Can be bypassed by direct URL access
def view(request):
    return render(request, 'template.html')
```

✓ **Right:** Using decorator
```python
# GOOD - Protected at view level
@login_required
@admin_required
def view(request):
    return render(request, 'template.html')
```

❌ **Wrong:** Forgetting @login_required
```python
# BAD - Unauthenticated users can access
@admin_required
def view(request):
    pass
```

✓ **Right:** Using both decorators
```python
# GOOD - Authenticated AND authorized
@login_required
@admin_required
def view(request):
    pass
```

## Debugging

Enable debug logging:
```python
import logging
logger = logging.getLogger(__name__)

@login_required
@admin_required
def view(request):
    logger.info(f"Admin access by {request.user.username}")
    pass
```

Check user profile:
```python
# In Django shell
user = User.objects.get(username='testuser')
print(user.profile.role)
print(user.profile.get_role_display())
```

## Support

For issues or questions about RBAC:
1. Check `ROLE_BASED_ACCESS_IMPLEMENTATION.md` for detailed docs
2. Review `core/decorators.py` for decorator implementation
3. Check `core/views.py` for view examples
4. Review `templates/base.html` for template patterns
