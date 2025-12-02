// Hospital Management System - JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Calculate bill total
function calculateBillTotal() {
    const consultationFee = parseFloat(document.getElementById('consultation_fee')?.value || 0);
    const roomCharges = parseFloat(document.getElementById('room_charges')?.value || 0);
    const medicineCharges = parseFloat(document.getElementById('medicine_charges')?.value || 0);
    const labCharges = parseFloat(document.getElementById('lab_charges')?.value || 0);
    const otherCharges = parseFloat(document.getElementById('other_charges')?.value || 0);
    const discount = parseFloat(document.getElementById('discount')?.value || 0);
    const tax = parseFloat(document.getElementById('tax')?.value || 0);

    const subtotal = consultationFee + roomCharges + medicineCharges + labCharges + otherCharges;
    const total = subtotal - discount + tax;

    if (document.getElementById('subtotal')) {
        document.getElementById('subtotal').value = subtotal.toFixed(2);
    }
    if (document.getElementById('total_amount')) {
        document.getElementById('total_amount').value = total.toFixed(2);
    }
}

// Search functionality
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        let found = false;
        const td = tr[i].getElementsByTagName('td');

        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }

        tr[i].style.display = found ? '' : 'none';
    }
}

// Print functionality
function printPage() {
    window.print();
}

// Export to PDF (requires jsPDF library)
function exportToPDF(elementId, filename) {
    const element = document.getElementById(elementId);
    if (element && typeof html2pdf !== 'undefined') {
        html2pdf()
            .from(element)
            .save(filename || 'document.pdf');
    } else {
        alert('PDF export functionality not available. Please use browser print.');
        window.print();
    }
}

// Date validation
function validateDate(inputId) {
    const input = document.getElementById(inputId);
    const selectedDate = new Date(input.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate < today) {
        alert('Please select a future date');
        input.value = '';
        return false;
    }
    return true;
}

// Check available time slots
function checkAvailableSlots(doctorId, date) {
    // This would typically make an AJAX call to check availability
    // For now, it's a placeholder
    console.log('Checking availability for doctor:', doctorId, 'on date:', date);
}

// Auto-calculate age from date of birth
function calculateAge(dobInputId, ageDisplayId) {
    const dobInput = document.getElementById(dobInputId);
    const ageDisplay = document.getElementById(ageDisplayId);

    if (dobInput && dobInput.value) {
        const dob = new Date(dobInput.value);
        const today = new Date();
        let age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
            age--;
        }

        if (ageDisplay) {
            ageDisplay.textContent = age + ' years';
        }
    }
}

// Format phone number
function formatPhoneNumber(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 10) {
            value = value.slice(0, 10);
        }
        input.value = value;
    }
}

// Medicine stock alert
function checkMedicineStock(stockQuantity, reorderLevel) {
    if (stockQuantity <= reorderLevel) {
        return 'low-stock';
    }
    return 'in-stock';
}

// Check medicine expiry
function checkMedicineExpiry(expiryDate) {
    const expiry = new Date(expiryDate);
    const today = new Date();
    const diffTime = expiry - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
        return 'expired';
    } else if (diffDays <= 30) {
        return 'expiring-soon';
    }
    return 'valid';
}

// Toggle sidebar on mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

// Initialize tooltips (Bootstrap)
document.addEventListener('DOMContentLoaded', function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize popovers (Bootstrap)
document.addEventListener('DOMContentLoaded', function () {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Real-time search
function setupRealtimeSearch(inputId, resultsContainerId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.addEventListener('input', function () {
            const query = this.value;
            // This would typically make an AJAX call
            console.log('Searching for:', query);
        });
    }
}

// File upload preview
function previewFile(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (input && input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            if (preview.tagName === 'IMG') {
                preview.src = e.target.result;
            } else {
                preview.innerHTML = '<img src="' + e.target.result + '" class="img-fluid" />';
            }
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// Dashboard stats animation
function animateStats() {
    const stats = document.querySelectorAll('.stats-card h3');
    stats.forEach(stat => {
        const target = parseInt(stat.textContent);
        let current = 0;
        const increment = target / 50;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// Call animation on page load
document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.stats-card')) {
        animateStats();
    }
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
