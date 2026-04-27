from doctors.models import DoctorProfile, DoctorAvailibility, BlockedSlot
from datetime import datetime, time


class SlotCalculationService:

    @staticmethod
    def get_avalible_slots(doctor_id, appointment_date):
        
        try:
            doctor = DoctorProfile.objects.get(id = doctor_id)
        except DoctorProfile.DoesNotExist:
            raise ValueError("Doctor not found")
        
        if appointment_date < datetime.now().date():
            raise ValueError("Appointment date must be in the future")
        
        day_of_week = appointment_date.weekday()
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

        blocked_slots = BlockedSlot.objects.filter(doctor = doctor_id, blocked_date = appointment_date)

        available_slots= []

        for slot in slots:  
            slot_start = slot['start_time']
            slot_end = slot['end_time']
            is_blocked = False
            for blocked in blocked_slots:
                if slot_start < blocked.end_time and slot_end > blocked.start_time:
                    is_blocked = True
            if is_blocked == False:
                available_slots.append(slot)
            

        return available_slots

    @staticmethod
    def _generate_slots(time_in, time_out, slot_duration):
        slots = []
        current_minutes = SlotCalculationService._time_to_minutes(time_in)
        end_minutes = SlotCalculationService._time_to_minutes(time_out)
        while current_minutes < end_minutes:
            slot_end_minutes = current_minutes + slot_duration
            if slot_end_minutes > end_minutes:
                break
            start_time = SlotCalculationService._minutes_to_time(current_minutes)
            end_time = SlotCalculationService._minutes_to_time(slot_end_minutes)
            slots.append({
                'start_time': start_time,
                'end_time': end_time,
            })
            current_minutes = slot_end_minutes
        return slots
        

    @staticmethod
    def _time_to_minutes(time_str):
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

