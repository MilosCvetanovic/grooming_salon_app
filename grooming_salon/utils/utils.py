from datetime import time, date, timedelta, datetime
import requests
from django.db.models import Avg, Count
from django.conf import settings
from django.template.loader import render_to_string

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
def get_rating_summary(reviews):
    total_reviews = reviews.count()
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    average_rating = format(round(average_rating, 1), ".1f")

    rating_distribution = reviews.values('rating').annotate(count=Count('rating'))
    rating_counts = {i: 0 for i in range(1, 6)}
    for item in rating_distribution:
        rating_counts[item['rating']] = item['count']

    rating_summary = []
    for star in range(5, 0, -1):
        count = rating_counts[star]
        percentage = round((count / total_reviews) * 100) if total_reviews > 0 else 0
        rating_summary.append({'star': star, 'count': count, 'percentage': percentage})

    return {
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'rating_summary': rating_summary,
    }

#-----------------------------------------------------------------------------------------------------------------------
def send_verification_email(user, token):
    verification_url = f'{settings.FRONTEND_URL}/accounts/verify/{token}/'

    html_content = render_to_string(
        'email_service/verification_email.html',
        {
            'profile_name': user.profile.get_profile_name,
            'verification_url': verification_url,
        }
    )

    response = requests.post(
        f'https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages',
        auth=('api', settings.MAILGUN_API_KEY),
        data={
            'from': f'Mila Salon za šišanje pasa <postmaster@{settings.MAILGUN_DOMAIN}>',
            'to': f"{user.profile.get_profile_name} <{user.email}>",
            'subject': "✅ Potvrdite vašu email adresu",
            'html': html_content,
        }
    )

    return response

#-----------------------------------------------------------------------------------------------------------------------
