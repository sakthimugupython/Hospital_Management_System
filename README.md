# Hospital Management System (HMS)

A comprehensive Hospital Management System built with Django, HTML, CSS, Bootstrap, and JavaScript.

## Features

### 1. **Authentication & User Management**
- Multi-role authentication (Admin, Doctor, Nurse, Receptionist, Pharmacist, Lab Technician)
- Role-based access control
- User profile management

### 2. **Patient Management**
- Add, edit, view, and delete patients
- Complete patient information (demographics, medical history, allergies)
- Patient medical records and reports
- Search functionality

### 3. **Doctor Management**
- Doctor profiles with specialization
- Consultation fees and schedules
- Available time slots
- Doctor performance tracking

### 4. **Appointment Booking**
- Create, approve, and cancel appointments
- Available time slot management
- Appointment status tracking (Pending, Approved, Completed, Cancelled)

### 5. **OPD (Out-Patient Department)**
- Patient vitals recording (BP, Temperature, Pulse, Weight)
- Symptoms and diagnosis
- Prescription management
- Treatment notes

### 6. **IPD (In-Patient Department)**
- Patient admission and discharge
- Bed allocation
- Daily rounds and treatment notes
- Admission history

### 7. **Ward & Bed Management**
- Multiple ward types (ICU, General, Private, Emergency)
- Bed status tracking (Vacant, Occupied, Maintenance)
- Real-time bed availability
- Ward-wise bed allocation

### 8. **Pharmacy Module**
- Medicine inventory management
- Stock tracking with reorder levels
- Expiry date monitoring
- Medicine dispensing
- Low stock alerts

### 9. **Laboratory Module**
- Lab test management
- Test request creation
- Result entry and report upload
- PDF/Image report support
- Test status tracking

### 10. **Billing System**
- Comprehensive billing with multiple charge types:
  - Consultation fees
  - Room charges
  - Medicine charges
  - Lab charges
  - Other charges
- Discount and tax calculation
- Multiple payment methods (Cash, Card, UPI, Insurance)
- Payment tracking
- Printable bills

### 11. **Staff Management**
- Staff registration with roles
- Attendance tracking
- Shift management
- Staff performance monitoring

### 12. **Reports & Analytics**
- Daily and monthly revenue reports
- Patient statistics
- Department-wise performance
- Doctor performance tracking
- Lab test summaries

### 13. **Dashboard**
- Real-time statistics
- Quick access to pending tasks
- Revenue tracking
- Bed availability
- Recent appointments

## Color Scheme
- Primary: #E67E22 (Orange)
- Secondary: #628141 (Green)
- Accent: #8BAE66 (Light Green)
- Light: #EBD5AB (Beige)

## Technology Stack
- **Backend**: Django 5.2.8
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, JavaScript
- **Database**: SQLite (Development)
- **Icons**: Font Awesome 6.4.0

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Navigate to project directory**
   ```bash
   cd e:\HMS
   ```

2. **Create and activate virtual environment** (if not already created)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Django** (if not already installed)
   ```bash
   pip install django pillow
   ```

4. **Run migrations** (Already completed)
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main Application: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Default Login Credentials
After creating a superuser, use those credentials to login.

## Project Structure
```
HMS/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── hms/                   # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── dashboard.html     # Dashboard
│   ├── login.html         # Login page
│   ├── patients/          # Patient templates
│   ├── doctors/           # Doctor templates
│   ├── appointments/      # Appointment templates
│   ├── opd/               # OPD templates
│   ├── ipd/               # IPD templates
│   ├── wards/             # Ward templates
│   ├── pharmacy/          # Pharmacy templates
│   ├── laboratory/        # Laboratory templates
│   ├── billing/           # Billing templates
│   ├── staff/             # Staff templates
│   ├── reports/           # Reports templates
│   └── errors/            # Error pages
├── static/                # Static files
│   ├── css/               # CSS files
│   └── js/                # JavaScript files
├── media/                 # User uploaded files
├── manage.py              # Django management script
└── db.sqlite3             # Database file
```

## Key Features Workflow

### Patient Registration → Appointment → Consultation → Pharmacy/Lab → Billing → Discharge

1. **Register Patient**: Add patient with complete details
2. **Book Appointment**: Schedule appointment with doctor
3. **OPD Consultation**: Doctor examines patient, records vitals, diagnosis, prescription
4. **Pharmacy**: Dispense medicines based on prescription
5. **Laboratory**: Conduct tests if required, upload reports
6. **Billing**: Generate comprehensive bill with all charges
7. **IPD (if required)**: Admit patient, allocate bed
8. **Discharge**: Discharge patient, free bed, final billing

## User Roles & Permissions

- **Admin**: Full system access
- **Doctor**: Patient consultation, prescriptions, medical records
- **Nurse**: Patient vitals, daily rounds, IPD care
- **Receptionist**: Patient registration, appointments, billing
- **Pharmacist**: Medicine inventory, dispensing
- **Lab Technician**: Lab tests, report uploads

## Important Notes

1. **No MD/TXT files**: All documentation is in this README
2. **Bootstrap Components**: Uses cards, tables, forms, modals, alerts
3. **Responsive Design**: Mobile-friendly layout
4. **Print Support**: Bills and reports are printable
5. **Error Handling**: Custom 404, 403, 500 pages
6. **Form Validation**: Client and server-side validation
7. **Search Functionality**: Available in patient and other modules
8. **Real-time Calculations**: Auto-calculate bill totals

## Development

To add sample data for testing:
1. Login to admin panel (http://127.0.0.1:8000/admin/)
2. Add sample patients, doctors, wards, medicines, lab tests
3. Test the complete workflow

## Support

For issues or questions, refer to Django documentation:
- Django Docs: https://docs.djangoproject.com/
- Bootstrap Docs: https://getbootstrap.com/docs/

## License

This project is created for educational and demonstration purposes.
