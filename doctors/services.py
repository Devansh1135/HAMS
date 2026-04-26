from doctors.models import DoctorProfile, DoctorAvailibility
from datetime import datetime, time


class SlotCalculationService:

    @staticmethod
    def get_avalible_slots(doctor_id, appointment_date):
        
        try:
            doctor = DoctorProfile.objects.get(id = doctor_id)
            print(doctor)
        except DoctorProfile.DoesNotExist:
            raise ValueError("Doctor not found")
        
        if appointment_date < datetime.now().date():
            raise ValueError("Appointment date must be in the future")
        
        day_of_week = appointment_date.weekday()
        print(day_of_week)
        try:
            from doctors.models import DoctorAvailibility
            availability = DoctorAvailibility.objects.get(
            doctor=doctor,
            days_of_week=day_of_week,
        )
            
        except DoctorAvailibility.DoesNotExist:
            return []


        slots = SlotCalculationService._generate_slots(
            str(availability.time_in), str(availability.time_out), availability.slot_duration
        )

        return slots

    @staticmethod
    def _generate_slots(time_in, time_out, slot_duration):
        print("Is ts even being called???")
        slots = []
        current_minutes = SlotCalculationService._time_to_minutes(time_in)
        end_minutes = SlotCalculationService._time_to_minutes(time_out)
        print(current_minutes, end_minutes, "is this thing on?")
        while current_minutes < end_minutes:
            slot_end_minutes = current_minutes + slot_duration
            if slot_end_minutes > end_minutes:
                break
            start_time = SlotCalculationService._minutes_to_time(current_minutes)
            print(type(start_time))
            end_time = SlotCalculationService._minutes_to_time(slot_end_minutes)
            slots.append({
                'start_time': start_time,
                'end_time': end_time,
            })
            current_minutes = slot_end_minutes
        return slots
        

    @staticmethod
    def _time_to_minutes(time_str):
        print("time_to_minutes called")
        parts = time_str.split(':')
        
        hours = int(parts[0])
        minutes = int(parts[1])
        return (hours * 60) + minutes

    @staticmethod
    def _minutes_to_time(minutes):
        hours = minutes // 60
        minutes = minutes % 60
        time_obj = time(hours,minutes)
        return time_obj

