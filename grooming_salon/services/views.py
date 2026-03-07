from datetime import date, time, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView
from grooming_salon.dogs.models import Dog, Note
from grooming_salon.services.models import Service, Groomer, Appointment
from grooming_salon.utils.mixins import UserOwnedModelMixin
from grooming_salon.utils.utils import validate_booking_step, get_upcoming_business_days, clear_booking_session

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class ServicesPageView(LoginRequiredMixin, TemplateView):
    template_name = 'services/services-page.html'

    # Želimo da ispraznimo sesiju u slučaju da smo redirektovani na početak zakazivanja
    def get(self, request, *args, **kwargs):
        self.request.session.pop('selected_services', None)
        return super().get(request, *args, **kwargs)

    # Šaljemo usluge 'services' strani kroz kontekst
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['selected_services'] = self.request.session.get('selected_services', [])
        return context

    # Čuvamo selektovane usluge u sesiji i redirektujemo na 'groomers' stranu
    def post(self, request, *args, **kwargs):
        selected_services = request.POST.getlist('services')

        if selected_services:
            request.session['selected_services'] = selected_services
            return redirect('groomers')

        return self.get(request, *args, **kwargs)

#-----------------------------------------------------------------------------------------------------------------------
class GroomerPageView(LoginRequiredMixin, View):
    template_name = 'services/groomers-page.html'

    # Osiguravamo da je pristup 'groomers' strani dozvoljen samo ako je prethodno izabrana usluga
    def dispatch(self, request, *args, **kwargs):
        if not validate_booking_step(request, 'groomer'):
            return redirect('services')
        return super().dispatch(request, *args, **kwargs)

    # Dohvatamo sve grumere i šaljemo kroz kontekst 'groomers' strani
    def get(self, request, *args, **kwargs):
        groomers = Groomer.objects.all()
        return render(request, self.template_name, {'groomers': groomers})

    # Pritiskom na dugme 'Izaberi' korisnik bira grumera (njegov 'id')
    # Proveravamo da li za taj 'id' zaista postoji grumer, ako ne postoji, vrati 404
    # Ako postoji, sačuvaj grumera u sesiji i redirektuj na 'appointments' stranu
    def post(self, request, *args, **kwargs):
        groomer_id = request.POST.get('groomer_id')
        groomer = get_object_or_404(Groomer, pk=groomer_id)
        request.session['selected_groomer'] = groomer_id
        return redirect('appointments')

#-----------------------------------------------------------------------------------------------------------------------
class AppointmentBookingView(LoginRequiredMixin, TemplateView):
    template_name = 'services/appointments-page.html'
    all_slots = [time(hour=h) for h in range(9, 17)]

    def dispatch(self, request, *args, **kwargs):
        # Osiguravamo da je pristup 'appointments' strani dozvoljen samo ako je prethodno izabran grumer
        if not validate_booking_step(request, 'appointment'):
            return redirect('groomers')
        return super().dispatch(request, *args, **kwargs)

    def get_groomer(self):
        groomer_id = self.request.session.get('selected_groomer')
        return get_object_or_404(Groomer, id=groomer_id)

    # Logika za datum
    def handle_date_selection(self, groomer):
        # Čitamo vrednost parametra 'date' iz URL-a
        selected_date_str = self.request.GET.get('date')

        if selected_date_str:
            try:
                # Konvertujemo string u 'Date' objekat
                selected_date = date.fromisoformat(selected_date_str)

                # U sesiji čuvamo datum na dva načina - za dalju obradu i za prikaz korisniku
                self.request.session.update({
                    'selected_date': selected_date_str,
                    'selected_date_display': selected_date.strftime('%d.%m.%Y.'),
                })
                # Reset selektovanog vremena kada korisnik menja datum
                self.request.session.pop('selected_time', None)
                self.request.session.pop('selected_time_display', None)

                # Vraćamo 'Date' objekat za template
                return selected_date

            except ValueError:
                pass

        return None

    # Logika za vreme
    def handle_time_selection(self):
        # Čitamo vrednost parametra 'time' iz URL-a
        selected_time = self.request.GET.get('time')

        # U sesiji čuvamo vreme kao string za dalju obradu i prikaz
        if selected_time and selected_time in self.all_slots:
            self.request.session['selected_time'] = selected_time

            return selected_time

        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groomer = self.get_groomer()

        # Dohvatamo sve termine koji su istekli i menjamo status na 'COMPLETED'
        Appointment.objects.mark_appointment_expired(groomer)

        selected_date = self.handle_date_selection(groomer)
        selected_time = self.handle_time_selection()

        # Dohvatamo sve termine i oslobađamo termine koji su otkazani
        unavailable_slots = Appointment.objects.free_cancelled_slots(groomer, selected_date)

        context.update({
            'dates': get_upcoming_business_days(),
            'selected_date': selected_date,
            'all_slots': self.all_slots,
            'unavailable_slots': unavailable_slots,
            'today': date.today(),
            'time_now': timezone.localtime().time(),
            'selected_time': selected_time,
        })
        return context

    # Osiguravamo da je jedino moguće preći na sledeću stranu onda kada su izabrani i datum i vreme
    def post(self, request, *args, **kwargs):
        if request.session.get('selected_date') and request.session.get('selected_time'):
            return redirect('dog_selection')

        # Ako uslovi nisu ispunjeni, ostajemo na stranici
        return self.get(request, *args, **kwargs)

#-----------------------------------------------------------------------------------------------------------------------
class DogSelectionView(LoginRequiredMixin, UserOwnedModelMixin, ListView):
    model = Dog
    template_name = 'services/dog-selection-page.html'
    context_object_name = 'dogs'

    # Osiguravamo da je pristup 'dog-selection' strani dozvoljen samo ako je prethodno izabran termin
    def dispatch(self, request, *args, **kwargs):
        if not validate_booking_step(request, 'dog_selection'):
            return redirect('appointments')
        return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return super().get_queryset()

    # Dohvatamo sve napomene i šaljemo ih templejtu kroz kontekst
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_notes'] = Note.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Pripremamo sve prikupljene podatke za kreiranje termina
        dog_id = request.POST.get('selected_dog')
        selected_notes_ids = request.POST.getlist('selected_notes')
        note_other_text = request.POST.get('note_other_text', '')

        service_ids = self.request.session.get('selected_services', [])
        services = Service.objects.filter(id__in=service_ids)

        groomer_id = request.session.get('selected_groomer')

        selected_date_str = request.sesion.get('selected_date')
        selected_time_str = request.session.get('selected_time')

        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        selected_time = datetime.strptime(selected_time_str, '%H:%M').time()

        # Proveravamo da li su svi neophodni podaci dostupni za kreiranje termina (napomena je opciona)
        if not all([service_ids, groomer_id, selected_date, selected_time, dog_id]):
            return render(request, self.template_name, {
                **self.get_context_data(),
                'error': 'Nedostaju podaci za zakazivanje. Molimo pokušajte ponovo.'
            })

        try:
            # Dohvatamo izabranog psa za konkretnog korisnika
            dog = get_object_or_404(Dog, id=dog_id, user=request.user)

            # Ako napomena postoji, dodajemo je konkretnom psu preko M2M relacije
            if selected_notes_ids:
                dog.notes.set(selected_notes_ids)

            # Kreiramo termin
            appointment = Appointment.objects.create(
                user=request.user,
                groomer_id=groomer_id,
                date=selected_date,
                time=selected_time,
                dog=dog,
                status='BOOKED',
            )

            # Dodajemo usluge u zakazani termin preko M2M relacije
            if services:
                appointment.services.set(services)

            # Pripremamo podatke u sesiji za prikaz na sledećoj strani
            selected_notes = Note.objects.filter(id__in=selected_notes_ids)
            session_notes = []

            # Beležimo napomene u listu
            for note in selected_notes:
                if note.condition == 'Drugo':
                    if note_other_text:
                        session_notes.append(note_other_text)
                else:
                    session_notes.append(note.condition)

            # Dodajemo izabranog psa i napomene u sesiji, ostali podaci se već nalaze u sesiji
            request.session['selected_dog_id'] = dog.id
            request.session['selected_notes'] = session_notes

            return redirect('confirmation')

        except IntegrityError:
            return render(request, self.template_name, {
                **self.get_context_data(),
                'error': 'Nažalost, ovaj termin je upravo zauzet.'
            })

#-----------------------------------------------------------------------------------------------------------------------
class ConfirmAppointmentView(LoginRequiredMixin, TemplateView):
    template_name = 'services/confirmation-page.html'

    # Osiguravamo da je pristup 'confirmation' strani dozvoljen samo ako je prethodno izabran pas
    def dispatch(self, request, *args, **kwargs):
        if not validate_booking_step(request, 'confirmation'):
            return redirect('dog_selection')
        return super().dispatch(request, *args, **kwargs)

    # Prosleđujemo templejut podatke sačuvane u sesiji kroz kontekst
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        services_ids = self.request.session.get('selected_services', [])
        groomer_id = self.request.session.get('selected_groomer')
        dog_id = self.request.session.get('selected_dog_id')

        if services_ids:
            context['services'] = Service.objects.filter(id__in=services_ids).all()

        if groomer_id:
            context['groomer'] = Groomer.objects.filter(id=groomer_id).first()

        if dog_id:
            context['dog'] = Dog.objects.filter(id=dog_id).first()

        context['date_display'] = self.request.session.get('selected_date')
        context['time_display'] = self.request.session.get('selected_time')
        context['notes_display'] = self.request.session.get('selected_notes')

        # Pozivamo utils funkciju za brisanje podataka iz sesije
        clear_booking_session(self.request)

        return context

#-----------------------------------------------------------------------------------------------------------------------
class MyAppointmentsView(LoginRequiredMixin, UserOwnedModelMixin, ListView):
    model = Appointment
    template_name = 'services/my-appointments-page.html'
    context_object_name = 'appointments'

    # UserOwned mixin filtrira sve Appointment objekte koji pripadaju trenutnom korisniku user=self.request.user
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Osvežavamo termine tako što ažuriramo status za one koji su se već završili
        for appoint in queryset.filter(status='BOOKED').prefetch_related('services'):
            appoint.mark_completed_if_past()

        # Vraćamo sortiran ceo set podataka potreban za prikaz detalja zakazanog termina
        return queryset.select_related('groomer', 'dog', 'review')\
            .prefetch_related('services')\
            .annotate(
                status_order=Case(
                    When(status='BOOKED', then=Value(1)),
                    When(status='COMPLETED', then=Value(2)),
                    When(status='CANCELLED', then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField(),
                )
            ).order_by('status_order', 'date', 'time')

#-----------------------------------------------------------------------------------------------------------------------
@login_required
def cancel_appointment(request, appointment_id):
    # Osiguravamo da trenutni korisnik može otkazati samo njegove termine
    appointment = get_object_or_404(Appointment.objects.prefetch_related('services'), id=appointment_id, user=request.user)

    # U suprotnom Error 405
    if request.method != 'POST':
        return render(request, '405.html', {'is_405': True}, status=405)

    # Zaštita od otkazivanja termina koji je već počeo
    appointment_start = timezone.make_aware(datetime.combine(appointment.date, appointment.time))
    if timezone.now() >= appointment_start:
        messages.error(request, 'Ne možete otkazati termin koji je već počeo.')
        return redirect('my_appointments')

    appointment.status = 'CANCELLED'
    appointment.save()

    return redirect('my_appointments')

#-----------------------------------------------------------------------------------------------------------------------
