from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('dashboard/nurse/', views.nurse_dashboard, name='nurse_dashboard'),
    path('dashboard/pharmacist/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('dashboard/lab-technician/', views.lab_technician_dashboard, name='lab_technician_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    
    # Patient Management
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_add, name='patient_add'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Doctor Management
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_add, name='doctor_add'),
    path('doctors/<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
    
    # Appointment Management
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_add, name='appointment_add'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/approve/', views.appointment_approve, name='appointment_approve'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    
    # OPD Management
    path('opd/', views.opd_list, name='opd_list'),
    path('opd/add/', views.opd_add, name='opd_add'),
    path('opd/<int:pk>/', views.opd_detail, name='opd_detail'),
    
    # IPD Management
    path('ipd/', views.ipd_list, name='ipd_list'),
    path('ipd/add/', views.ipd_add, name='ipd_add'),
    path('ipd/<int:pk>/discharge/', views.ipd_discharge, name='ipd_discharge'),
    
    # Ward and Bed Management
    path('wards/', views.ward_list, name='ward_list'),
    path('wards/add/', views.ward_add, name='ward_add'),
    path('beds/', views.bed_list, name='bed_list'),
    
    # Pharmacy Management
    path('pharmacy/medicines/', views.medicine_list, name='medicine_list'),
    path('pharmacy/medicines/add/', views.medicine_add, name='medicine_add'),
    path('pharmacy/medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    
    # Laboratory Management
    path('laboratory/tests/', views.lab_test_list, name='lab_test_list'),
    path('laboratory/tests/add/', views.lab_test_add, name='lab_test_add'),
    path('laboratory/requests/', views.lab_request_list, name='lab_request_list'),
    path('laboratory/requests/add/', views.lab_request_add, name='lab_request_add'),
    path('laboratory/requests/<int:pk>/update/', views.lab_request_update, name='lab_request_update'),
    
    # Billing Management
    path('billing/', views.bill_list, name='bill_list'),
    path('billing/add/', views.bill_add, name='bill_add'),
    path('billing/<int:pk>/', views.bill_detail, name='bill_detail'),
    path('billing/<int:pk>/payment/', views.bill_payment, name='bill_payment'),
    
    # Staff Management
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_add, name='staff_add'),
    path('staff/attendance/', views.attendance_list, name='attendance_list'),
    path('staff/attendance/mark/', views.attendance_mark, name='attendance_mark'),
    
    # Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
