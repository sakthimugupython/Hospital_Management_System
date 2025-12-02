from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(*allowed_roles):
    """
    Decorator to check if user has required role.
    Usage: @role_required('admin', 'doctor')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                user_role = request.user.profile.role
            except:
                messages.error(request, 'User profile not found.')
                return redirect('login')
            
            if user_role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    """Decorator to restrict access to admin only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'admin':
                messages.error(request, 'Admin access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def doctor_required(view_func):
    """Decorator to restrict access to doctors only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'doctor':
                messages.error(request, 'Doctor access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def receptionist_required(view_func):
    """Decorator to restrict access to receptionists only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'receptionist':
                messages.error(request, 'Receptionist access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def nurse_required(view_func):
    """Decorator to restrict access to nurses only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'nurse':
                messages.error(request, 'Nurse access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def pharmacist_required(view_func):
    """Decorator to restrict access to pharmacists only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'pharmacist':
                messages.error(request, 'Pharmacist access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def lab_technician_required(view_func):
    """Decorator to restrict access to lab technicians only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'lab_technician':
                messages.error(request, 'Lab Technician access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def patient_required(view_func):
    """Decorator to restrict access to patients only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role != 'patient':
                messages.error(request, 'Patient access required.')
                return redirect('dashboard')
        except:
            messages.error(request, 'User profile not found.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper
