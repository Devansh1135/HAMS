# Hospital Appointment Management System - API Structure & Workflow

## 1. PHASE-WISE DEVELOPMENT ROADMAP

### Phase 1: Authentication & User Management (Foundation)
**Status**: ✅ Partially Complete - `/auth/signup/` exists
**Priority**: HIGH - Complete before moving forward
- [ ] `POST /api/auth/signup/` - Patient signup (Done) -- done
- [ ] `POST /api/auth/login/` - User login (Email/Phone + Password) -- done
- [ ] `POST /api/auth/logout/` - User logout -- done
- [ ] `POST /api/auth/refresh/` - Refresh token -- done
- [ ] `GET /api/auth/me/` - Get current user profile -- done
- [ ] `POST /api/auth/password-change/` - Change password -- done
- [ ] `POST /api/auth/password-reset/` - Password reset (optional) -- pending

### Phase 2: Patient Profile Management
**Status**: ⏳ Pending
**Priority**: HIGH
- [ ] `GET /api/patients/me/` - Get own profile
- [ ] `PUT /api/patients/me/` - Update own profile
- [ ] `GET /api/patients/<id>/` - Get patient profile (admin only)

### Phase 3: Doctor Management (Admin + Doctor Operations)
**Status**: ⏳ Pending
**Priority**: HIGH
- [ ] `POST /api/doctors/` - Create doctor (Admin only) -- done
- [ ] `GET /api/doctors/` - List doctors (Paginated, Filterable) -- done
- [ ] `GET /api/doctors/<id>/` - Get doctor details (Public) -- done
- [ ] `PUT /api/doctors/<id>/` - Update doctor profile (Doctor owns or Admin) -- done
- [ ] `DELETE /api/doctors/<id>/` - Delete doctor (Admin only) -- done

### Phase 4: Doctor Availability Management
**Status**: ⏳ Pending
**Priority**: HIGH
- [ ] `POST /api/doctors/<id>/availability/` - Create availability schedule -- done
- [ ] `GET /api/doctors/<id>/availability/` - Get availability rules -- done
- [ ] `PUT /api/doctors/<id>/availability/<avail_id>/` - Update availability -- done
- [ ] `GET /api/doctors/<id>/availability/<avail_id>/` - Retrieve availability -- done
- [ ] `DELETE /api/doctors/<id>/availability/<avail_id>/` - Delete availability -- done

### Phase 5: Slot Management (Critical for Booking)
**Status**: ⏳ Pending (This will be computed, not stored)
**Priority**: CRITICAL
- [ ] `GET /api/doctors/<id>/slots/?date=YYYY-MM-DD` - Get available slots for doctor on date -- done
  - This endpoint will calculate slots dynamically based on availability + blocked slots

### Phase 6: Blocked Slots Management
**Status**: ⏳ Pending
**Priority**: MEDIUM
- [ ] `POST /api/doctors/<id>/blocked-slots/` - Block a slot (Doctor only) -- done
- [ ] `GET /api/doctors/<id>/blocked-slots/` - List blocked slots -- done
- [ ] `DELETE /api/doctors/<id>/blocked-slots/<id>/` - Unblock a slot -- done

### Phase 7: Appointment Booking & Management
**Status**: ⏳ Pending
**Priority**: CRITICAL
- [ ] `POST /api/appointments/` - Book appointment (Patient only)
- [ ] `GET /api/appointments/` - List appointments (Patient sees own, Doctor sees their appointments)
- [ ] `GET /api/appointments/<id>/` - Get appointment details
- [ ] `PUT /api/appointments/<id>/` - Update appointment (cancel, reschedule, etc.)
- [ ] `DELETE /api/appointments/<id>/` - Cancel appointment
- [ ] `GET /api/doctors/<id>/appointments/` - Get doctor's appointments (Doctor only)

### Phase 8: Optional Enhancements
**Status**: ⏳ Pending
**Priority**: LOW
- [ ] Appointment history & analytics
- [ ] Email/SMS notifications
- [ ] Review/Rating system
- [ ] Admin dashboard endpoints

---

## 2. DETAILED API ENDPOINT STRUCTURE

### Authentication Module (`accounts` app)

```
POST /api/auth/signup/
├─ Body: { email, phone, password, password_confirm, first_name, last_name }
├─ Response: { id, email, token, refresh_token, user_type }
└─ Logic: Create User + PatientProfile

POST /api/auth/login/
├─ Body: { email/phone, password }
├─ Response: { token, refresh_token, user_type, profile_id }
└─ Logic: Authenticate user, return tokens

POST /api/auth/logout/
├─ Headers: Authorization: Bearer <token>
├─ Response: { message: "Logged out successfully" }
└─ Logic: Blacklist token (optional, depends on JWT strategy)

POST /api/auth/refresh/
├─ Body: { refresh_token }
├─ Response: { access_token, refresh_token }
└─ Logic: Issue new access token

GET /api/auth/me/
├─ Headers: Authorization: Bearer <token>
├─ Response: { User data + Profile data (polymorphic) }
└─ Logic: Return current user and their profile
```

### Patient Profile Module (`accounts` app)

```
GET /api/patients/me/
├─ Headers: Authorization: Bearer <token>
├─ Permissions: IsAuthenticated, IsPatient
├─ Response: { id, user_info, phone, address, date_of_birth, medical_history, etc. }
└─ Logic: Return authenticated patient's profile

PUT /api/patients/me/
├─ Headers: Authorization: Bearer <token>
├─ Body: { phone, address, date_of_birth, medical_history, ... }
├─ Permissions: IsAuthenticated, IsPatient
└─ Logic: Update patient's own profile
```

### Doctor Management Module (`doctors` app)

```
GET /api/doctors/
├─ Query Params: ?search=name&specialization=&page=1&page_size=10
├─ Response: { count, next, previous, results: [...] }
├─ Permissions: AllowAny (public endpoint)
└─ Logic: List all active doctors with pagination/filtering

GET /api/doctors/<id>/
├─ Permissions: AllowAny
├─ Response: { id, name, specialization, qualification, phone, bio, avg_rating, ... }
└─ Logic: Get doctor details (public info only)

POST /api/doctors/
├─ Body: { user_email, specialization, qualification, phone, bio, license_number, ... }
├─ Permissions: IsAuthenticated, IsAdmin
└─ Logic: Create new doctor (Admin creates User + DoctorProfile)

PUT /api/doctors/<id>/
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
├─ Body: { specialization, qualification, bio, phone, ... }
└─ Logic: Update doctor profile

DELETE /api/doctors/<id>/
├─ Permissions: IsAuthenticated, IsAdmin
└─ Logic: Soft delete doctor (set is_active=False)
```

### Doctor Availability Module (`doctors` app)

```
POST /api/doctors/<doctor_id>/availability/
├─ Body: {
│   day_of_week: 0-6 (0=Monday, 6=Sunday),
│   time_in: "09:00",
│   time_out: "17:00",
│   slot_duration_minutes: 30
│ }
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Create availability schedule for a day

GET /api/doctors/<doctor_id>/availability/
├─ Permissions: AllowAny
├─ Response: [{ id, day_of_week, time_in, time_out, slot_duration_minutes }, ...]
└─ Logic: Get all availability schedules for a doctor

PUT /api/doctors/<doctor_id>/availability/<id>/
├─ Body: { day_of_week, time_in, time_out, slot_duration_minutes }
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Update availability schedule

DELETE /api/doctors/<doctor_id>/availability/<id>/
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Delete availability schedule
```

### Slots Endpoint - Dynamic Calculation (CRITICAL)

```
GET /api/doctors/<doctor_id>/slots/?date=YYYY-MM-DD
├─ Query Params: date (required), time_zone (optional)
├─ Permissions: AllowAny
├─ Response: {
│   doctor_id,
│   date,
│   available_slots: [
│     { slot_id, start_time, end_time, is_available },
│     { slot_id, start_time, end_time, is_available },
│     ...
│   ]
│ }
└─ Logic:
    1. Get DoctorAvailability for requested date's day_of_week
    2. If no availability exists, return empty slots
    3. Generate all slots between time_in and time_out based on slot_duration
    4. Filter out slots that have Appointments or BlockedSlots
    5. Return available slots
```

### Blocked Slots Module (`doctors` app)

```
POST /api/doctors/<doctor_id>/blocked-slots/
├─ Body: {
│   start_time: "2024-12-25T10:00:00Z",
│   end_time: "2024-12-25T11:00:00Z",
│   reason: "Break/Personal reason"
│ }
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Block a time slot

GET /api/doctors/<doctor_id>/blocked-slots/
├─ Query Params: ?date=YYYY-MM-DD (optional)
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Get all blocked slots (optionally filtered by date)

DELETE /api/doctors/<doctor_id>/blocked-slots/<id>/
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
└─ Logic: Remove blocked slot
```

### Appointments Module (`appointments` app)

```
POST /api/appointments/
├─ Body: {
│   doctor_id,
│   appointment_date: "YYYY-MM-DD",
│   slot_start_time: "HH:MM:SS",
│   reason: "Checkup"
│ }
├─ Permissions: IsAuthenticated, IsPatient
├─ Response: { id, doctor, appointment_date, slot_start_time, status, created_at }
├─ Validations:
│   - Slot must be available (not blocked, not booked)
│   - Appointment date must be in future
│   - Patient can't have duplicate appointments
└─ Logic:
    1. Validate doctor exists and is active
    2. Check slot availability using slots calculation logic
    3. Create Appointment with status='SCHEDULED'
    4. Send confirmation (email/SMS)

GET /api/appointments/
├─ Query Params: ?status=SCHEDULED&date_from=&doctor_id= (optional filters)
├─ Permissions: IsAuthenticated
├─ Response: [{ id, doctor, patient, appointment_date, status, ... }, ...]
├─ Logic:
    - Patients see only their appointments
    - Doctors see their appointments (via different endpoint)
    - Admin sees all appointments

GET /api/appointments/<id>/
├─ Permissions: IsAuthenticated, (IsAppointmentOwner OR IsDoctor OR IsAdmin)
├─ Response: Full appointment details
└─ Logic: Detailed view with patient & doctor info

PUT /api/appointments/<id>/
├─ Body: { status } or { appointment_date, slot_start_time }
├─ Permissions: IsAuthenticated, (IsAppointmentOwner OR IsDoctor OR IsAdmin)
├─ Possible Status Changes:
│   - SCHEDULED → COMPLETED (Doctor only, after appointment)
│   - SCHEDULED → CANCELLED (Patient or Doctor)
│   - SCHEDULED → RESCHEDULED (if changing date/time)
└─ Logic:
    - Validate status transition
    - If rescheduling, check slot availability
    - Update appointment

DELETE /api/appointments/<id>/
├─ Permissions: IsAuthenticated, (IsAppointmentOwner OR IsAdmin)
├─ Logic: Soft delete appointment (set status=CANCELLED)

GET /api/doctors/<doctor_id>/appointments/
├─ Query Params: ?status=SCHEDULED&date_from=
├─ Permissions: IsAuthenticated, (IsDoctorOwner OR IsAdmin)
├─ Response: List of doctor's appointments
└─ Logic: Get appointments for specific doctor
```

---

## 3. DATABASE MODELS - FINAL STRUCTURE

### Accounts App

```python
# User Model (Extended Django User)
class User(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, unique=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# PatientProfile Model
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Doctors App

```python
# DoctorProfile Model
class DoctorProfile(models.Model):
    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        # ... add more
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# DoctorAvailability Model
class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    time_in = models.TimeField()
    time_out = models.TimeField()
    slot_duration_minutes = models.IntegerField(default=30)  # in minutes
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('doctor', 'day_of_week')  # One schedule per day per doctor

# BlockedSlot Model (NEW)
class BlockedSlot(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='blocked_slots')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['doctor', 'start_datetime']),
        ]
```

### Appointments App

```python
# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No Show'),
    )
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()  # Start time of the slot
    slot_end_time = models.TimeField()  # Calculated from slot_duration
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.CharField(max_length=255)
    notes = models.TextField(blank=True)  # Doctor's notes after appointment
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')
        indexes = [
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date']),
        ]
```

---

## 4. IMPLEMENTATION ORDER & CHECKLIST

### Step 1: Create Models (1-2 hours)
- [ ] Create `BlockedSlot` model in `doctors` app
- [ ] Verify all model relationships and constraints
- [ ] Run migrations
- [ ] Create Django admin interfaces for all models

### Step 2: Create Serializers (2-3 hours)
Location: Create `serializers.py` in each app

**accounts/serializers.py**
- `UserSerializer` - Basic user data
- `PatientSignupSerializer` - For signup endpoint
- `PatientProfileSerializer` - Patient profile details
- `LoginSerializer` - For login validation

**doctors/serializers.py**
- `DoctorProfileSerializer` - Doctor info
- `DoctorAvailabilitySerializer` - Availability schedule
- `BlockedSlotSerializer` - Blocked slots
- `AvailableSlotsSerializer` - Response for slots endpoint

**appointments/serializers.py**
- `AppointmentSerializer` - Full appointment data
- `AppointmentCreateSerializer` - For creating appointments
- `AppointmentUpdateSerializer` - For updating status/rescheduling

### Step 3: Create Permissions & Authentication (1-2 hours)
Location: Create `permissions.py` in each app

**accounts/permissions.py**
```python
class IsPatient(permissions.BasePermission)
class IsDoctorUser(permissions.BasePermission)
class IsAdmin(permissions.BasePermission)
```

**doctors/permissions.py**
```python
class IsDoctorOwner(permissions.BasePermission)  # Doctor can only edit own profile
```

**appointments/permissions.py**
```python
class IsAppointmentOwner(permissions.BasePermission)  # Patient can only see own appointments
class IsAppointmentDoctor(permissions.BasePermission)  # Doctor can only see their appointments
```

### Step 4: Implement Authentication Views (2-3 hours)
Location: `accounts/views.py`

- `SignupView` (Already done)
- `LoginView`
- `LogoutView`
- `RefreshTokenView`
- `UserProfileView`

**Use JWT tokens:**
```bash
pip install djangorestframework-simplejwt
```

### Step 5: Implement Doctor Management Views (2-3 hours)
Location: `doctors/views.py`

- `DoctorListView` (GET, search, filter)
- `DoctorDetailView` (GET doctor info)
- `DoctorCreateView` (POST, admin only)
- `DoctorUpdateView` (PUT, doctor or admin)

### Step 6: Implement Availability Management Views (2-3 hours)
Location: `doctors/views.py`

- `AvailabilityCreateView` (POST)
- `AvailabilityListView` (GET)
- `AvailabilityUpdateView` (PUT)
- `AvailabilityDeleteView` (DELETE)

### Step 7: Implement Slot Calculation Logic (3-4 hours) ⭐ CRITICAL
Location: `doctors/utils.py` or `doctors/services.py`

Create a utility function:
```python
def get_available_slots(doctor_id, appointment_date):
    """
    Calculate available slots for a doctor on a given date
    
    Logic:
    1. Get day of week from appointment_date
    2. Query DoctorAvailability for that day
    3. Generate all possible slots between time_in and time_out
    4. Filter out booked appointments
    5. Filter out blocked slots
    6. Return list of available slots with start/end times
    """
```

Then create view:
- `AvailableSlotsView` (GET with date parameter)

### Step 8: Implement Blocked Slots Views (1-2 hours)
Location: `doctors/views.py`

- `BlockedSlotCreateView` (POST)
- `BlockedSlotListView` (GET)
- `BlockedSlotDeleteView` (DELETE)

### Step 9: Implement Appointment Views (3-4 hours) ⭐ CRITICAL
Location: `appointments/views.py`

- `AppointmentCreateView` (POST)
  - Validate slot availability
  - Create appointment
  - Send confirmation
  
- `AppointmentListView` (GET)
  - Filter by patient/doctor
  - Apply status filters
  
- `AppointmentDetailView` (GET)
- `AppointmentUpdateView` (PUT)
  - Handle status changes
  - Handle rescheduling
  
- `AppointmentCancelView` (DELETE or PATCH)

### Step 10: Create URL Routing (1 hour)
Location: Create/Update `urls.py` files

**accounts/urls.py**
```python
path('auth/signup/', SignupView.as_view()),
path('auth/login/', LoginView.as_view()),
path('auth/logout/', LogoutView.as_view()),
path('auth/refresh/', RefreshTokenView.as_view()),
path('auth/me/', UserProfileView.as_view()),
path('patients/me/', PatientProfileView.as_view()),
```

**doctors/urls.py**
```python
path('doctors/', DoctorListView.as_view()),
path('doctors/<int:pk>/', DoctorDetailView.as_view()),
path('doctors/<int:doctor_id>/availability/', AvailabilityListCreateView.as_view()),
path('doctors/<int:doctor_id>/availability/<int:id>/', AvailabilityUpdateDeleteView.as_view()),
path('doctors/<int:doctor_id>/slots/', AvailableSlotsView.as_view()),
path('doctors/<int:doctor_id>/blocked-slots/', BlockedSlotListCreateView.as_view()),
path('doctors/<int:doctor_id>/blocked-slots/<int:id>/', BlockedSlotDeleteView.as_view()),
```

**appointments/urls.py**
```python
path('appointments/', AppointmentListCreateView.as_view()),
path('appointments/<int:pk>/', AppointmentDetailView.as_view()),
path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view()),
path('doctors/<int:doctor_id>/appointments/', DoctorAppointmentListView.as_view()),
```

### Step 11: Add Validation & Error Handling (1-2 hours)
- Validate all appointment date/time constraints
- Handle timezone conversions
- Proper error responses
- Add request validation serializers

### Step 12: Testing (2-3 hours)
- Write unit tests for slot calculation logic
- Test appointment booking flow
- Test permission checks
- Test edge cases (double booking, past dates, etc.)

---

## 5. KEY BUSINESS LOGIC TO IMPLEMENT

### Slot Calculation Algorithm
```
Input: doctor_id, appointment_date
Output: List of available slots

ALGORITHM:
1. Get day_of_week from appointment_date (0=Monday, 6=Sunday)
2. Query DoctorAvailability.objects.filter(doctor_id=doctor_id, day_of_week=day_of_week)
3. If no availability found:
   return [] (no slots available)
4. Get time_in, time_out, slot_duration_minutes from availability
5. current_time = time_in
6. slots = []
7. While current_time < time_out:
   - slot_end = current_time + slot_duration_minutes
   - If slot_end > time_out:
     break
   - slots.append({
       start_time: current_time,
       end_time: slot_end,
       is_available: True
     })
   - current_time = slot_end
8. For each slot in slots:
   - Check if Appointment exists for (doctor, appointment_date, slot.start_time)
   - Check if BlockedSlot exists overlapping with slot
   - If either exists, mark is_available = False
9. Return slots
```

### Appointment Booking Validation
```
Before creating appointment, validate:
1. ✓ Doctor exists and is_active = True
2. ✓ Patient exists
3. ✓ Appointment date is in the future
4. ✓ Appointment date is not in the past
5. ✓ No existing appointment for same patient+doctor+datetime
6. ✓ Slot is available (use slot calculation logic)
7. ✓ No overlapping blocked slots
```

### Status Transition Rules
```
scheduled → completed (Doctor only, after appointment date)
scheduled → cancelled (Patient or Doctor, anytime)
scheduled → no-show (Doctor, after appointment date without completion)
completed → (no transitions)
cancelled → (no transitions)
```

---

## 6. RECOMMENDED UTILITIES & HELPERS

### appointments/utils.py
```python
from datetime import datetime, timedelta

def get_appointment_datetime(date, time):
    """Combine date and time into datetime"""
    return datetime.combine(date, time)

def is_future_datetime(date, time):
    """Check if appointment is in the future"""
    appointment_dt = get_appointment_datetime(date, time)
    return appointment_dt > datetime.now()

def validate_appointment_date(date):
    """Validate appointment date"""
    if date < date.today():
        raise ValueError("Appointment date must be in the future")
```

### doctors/utils.py
```python
def get_available_slots(doctor_id, appointment_date):
    """Main slot calculation logic"""
    # Implementation as per algorithm above
    pass

def check_slot_overlap(blocked_slots, slot_start, slot_end):
    """Check if a slot overlaps with any blocked slots"""
    pass

def calculate_slot_end_time(start_time, duration_minutes):
    """Calculate slot end time"""
    pass
```

---

## 7. CONFIGURATION & SETTINGS

### requirements.txt additions
```
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
python-decouple==3.8
django-cors-headers==4.3.0
```

### settings.py
```python
INSTALLED_APPS = [
    'drf_spectacular',  # API docs
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'accounts',
    'doctors',
    'appointments',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

---

## 8. API TESTING FLOW (Manual Testing Sequence)

### 1. Patient Signup & Login
```bash
POST /api/auth/signup/
{
  "email": "patient@example.com",
  "phone": "9999999999",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}

Response: { token, refresh_token, user_type: "patient" }
```

### 2. Admin: Create Doctor
```bash
POST /api/doctors/
Headers: Authorization: Bearer <admin_token>
{
  "user_email": "doctor@example.com",
  "specialization": "cardiology",
  "qualification": "MD, DM",
  "phone": "8888888888",
  "license_number": "LIC123456"
}
```

### 3. Doctor: Set Availability
```bash
POST /api/doctors/<doctor_id>/availability/
Headers: Authorization: Bearer <doctor_token>
{
  "day_of_week": 0,  # Monday
  "time_in": "09:00:00",
  "time_out": "17:00:00",
  "slot_duration_minutes": 30
}
```

### 4. Patient: View Available Slots
```bash
GET /api/doctors/<doctor_id>/slots/?date=2024-12-16
Headers: Authorization: Bearer <patient_token>

Response: {
  "doctor_id": 1,
  "date": "2024-12-16",
  "available_slots": [
    { "slot_id": "1", "start_time": "09:00", "end_time": "09:30", "is_available": true },
    { "slot_id": "2", "start_time": "09:30", "end_time": "10:00", "is_available": true },
    ...
  ]
}
```

### 5. Patient: Book Appointment
```bash
POST /api/appointments/
Headers: Authorization: Bearer <patient_token>
{
  "doctor_id": 1,
  "appointment_date": "2024-12-16",
  "appointment_time": "09:00:00",
  "reason": "Regular checkup"
}

Response: { id, doctor, appointment_date, appointment_time, status: "scheduled" }
```

### 6. Patient: View Booked Appointments
```bash
GET /api/appointments/
Headers: Authorization: Bearer <patient_token>

Response: [{ Appointment details }, ...]
```

### 7. Doctor: Block a Slot
```bash
POST /api/doctors/<doctor_id>/blocked-slots/
Headers: Authorization: Bearer <doctor_token>
{
  "start_datetime": "2024-12-16T12:00:00Z",
  "end_datetime": "2024-12-16T13:00:00Z",
  "reason": "Lunch break"
}
```

### 8. Patient: Try to Book Already-Booked Slot (Should Fail)
```bash
POST /api/appointments/
Headers: Authorization: Bearer <patient_token>
{
  "doctor_id": 1,
  "appointment_date": "2024-12-16",
  "appointment_time": "09:00:00",  # Already booked
  "reason": "Checkup"
}

Response: 400 Bad Request { error: "Slot is not available" }
```

---

## 9. COMMON PITFALLS TO AVOID

1. **Timezone Issues**: Always work with UTC internally, convert to local time only for display
2. **Race Conditions**: Use database transactions for appointment creation
3. **Slot Overlap**: Verify no overlaps between blocked slots and appointments
4. **Past Appointments**: Prevent booking appointments in the past
5. **Duplicate Bookings**: Use unique constraint on (doctor, date, time)
6. **Availability Not Set**: Handle case when doctor has no availability for requested date
7. **Permission Checks**: Always verify user permissions in views
8. **Serializer Validation**: Use serializer-level validation for complex business rules

---

## 10. NEXT IMMEDIATE STEPS

1. **Create BlockedSlot Model** and migrate
2. **Create all Serializers** in their respective apps
3. **Create Permissions Classes** in each app
4. **Implement LoginView** in accounts app
5. **Implement DoctorListView** and **DoctorDetailView**
6. **Implement AvailabilityViews** (CRUD)
7. **Create slot calculation utility function** and **AvailableSlotsView**
8. **Implement AppointmentCreateView with full validation**
9. **Test the complete booking flow end-to-end**

---

**Total Estimated Development Time**: 30-40 hours for core functionality

Good luck! Start with Phase 1 & 2, ensure authentication works flawlessly before moving to Phase 3+.
