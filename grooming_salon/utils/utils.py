from datetime import time, date, timedelta, datetime

WORK_START = time(9, 0)
WORK_END = time(17, 0)
HOURS = 1
WORKING_DAYS = 6

#-----------------------------------------------------------------------------------------------------------------------
# Vraća True ako su svi potrebni podaci za dati korak prisutni u sesiji.
def validate_booking_step(request, step_name):
    steps = {
        'groomer': ['selected_services'],
        'appointment': ['selected_groomer'],
        'dog_selection': ['selected_date', 'selected_time'],
        'confirmation': ['selected_dog_id']
    }

    required_keys = steps.get(step_name, [])

    return all(request.session.get(key) for key in required_keys)

#-----------------------------------------------------------------------------------------------------------------------
# Generišemo listu nadolazećih 7 radnih dana, isključujući Nedelju
def get_upcoming_business_days(start_date=None, days_count=7):
    if start_date is None:
        start_date = date.today()

    dates = []
    current_date = start_date

    for i in range(days_count):
        d = current_date + timedelta(days=i)
        if d.weekday() != WORKING_DAYS:  # 6 je Nedelja
            dates.append(d)

    return dates

#-----------------------------------------------------------------------------------------------------------------------
# Generišemo listu dnevnih dostupnih termina u periodu od 09:00h - 16:00h
def generate_daily_slots():
    slots = []
    current = datetime.combine(datetime.today(), WORK_START)
    end = datetime.combine(datetime.today(), WORK_END)

    while current < end:
        slots.append(current.time())
        current += timedelta(hours=HOURS)

    return slots

#-----------------------------------------------------------------------------------------------------------------------
# Brišemo podatke sačuvane u sesiji
BOOKING_SESSION_KEYS = [
    'selected_services', 'selected_groomer', 'selected_date', 'selected_time',
    'selected_date_display', 'selected_dog_id', 'selected_notes',
]

def clear_booking_session(request):
    for key in BOOKING_SESSION_KEYS:
        request.session.pop(key, None)

#-----------------------------------------------------------------------------------------------------------------------
