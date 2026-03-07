from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import OuterRef, Exists, Count, Value
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from grooming_salon.reviews.forms import ReviewForm
from grooming_salon.reviews.models import Review, ReviewLike
from grooming_salon.services.models import Appointment
from grooming_salon.utils.mixins import ImageCleanupMixin
from grooming_salon.utils.utils import get_rating_summary

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class AddReviewView(LoginRequiredMixin, ImageCleanupMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review-add-page.html'
    success_url = reverse_lazy('my_appointments')

    # Osiguravamo da termin pripada ulogovanom korisniku i da ne moze dodati recenziju za drugog korisnika
    def get_appointment(self):
        if not hasattr(self, '_appointment'):
            self._appointment = get_object_or_404(
                Appointment,
                id=self.kwargs.get('appointment_id'),
                user=self.request.user
            )
        return self._appointment

    # Proveravamo da li je recenzija već dodata za datu recenziju, ako jeste redirektuj na Edit te recenzije
    def dispatch(self, request, *args, **kwargs):
        appointment = self.get_appointment()

        if hasattr(appointment, 'review'):
            return redirect('edit_review', appointment_id=appointment.id)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Uveži recenziju sa terminom pre čuvanja u bazi
        form.instance.appointment = self.get_appointment()

        # ImageCleanup Mixin validira da li je slika obrisana kada korisnik aktivira (X)
        if self.handle_image_cleanup(form):
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.get_appointment()
        return context

# -----------------------------------------------------------------------------------------------------------------------
class EditReviewView(LoginRequiredMixin, PermissionRequiredMixin, ImageCleanupMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review-edit-page.html'
    success_url = reverse_lazy('review_details')
    permission_required = 'reviews.change_review'

    # Dohvati recenziju koja je povezana sa datim terminom
    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get('appointment_id')

        return get_object_or_404(
            Review,
            appointment_id=appointment_id,
            appointment__user=self.request.user
        )

    def form_valid(self, form):
        appointment_id = self.kwargs.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id, user=self.request.user)

        # Uveži recenziju sa terminom pre čuvanja u bazi
        form.instance.appointment = appointment

        # ImageCleanup Mixin validira da li je slika obrisana kada korisnik aktivira (X)
        if self.handle_image_cleanup(form):
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

# -----------------------------------------------------------------------------------------------------------------------
class DeleteReviewView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review-delete-page.html'
    success_url = reverse_lazy('review_details')
    permission_required = 'reviews.delete_review'

    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get('appointment_id')

        return get_object_or_404(
            Review,
            appointment_id=appointment_id,
            appointment__user=self.request.user
        )

# -----------------------------------------------------------------------------------------------------------------------
class ReviewDetailsView(ListView):
    model = Review
    template_name = 'reviews/all-reviews-page.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = (Review.objects.select_related('appointment__user__profile').
                    annotate(likes_count=Count('likes')))

        # Ako je korisnik ulogovan, dodajemo atribut 'user_has_liked' svakoj recenziji
        user = self.request.user

        if user.is_authenticated:
            # Proveravamo da li postoji lajk ovog korisnika za ovu recenziju
            user_likes = ReviewLike.objects.filter(user=user, to_review=OuterRef('pk'))
            queryset = queryset.annotate(user_has_liked=Exists(user_likes))
        else:
            queryset = queryset.annotate(user_has_liked=Value(False))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_rating_summary(context['reviews']))
        return context

# -----------------------------------------------------------------------------------------------------------------------
class ReviewLikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=kwargs['review_pk'])

        like, created = ReviewLike.objects.get_or_create(to_review=review, user=request.user)

        if not created:
            like.delete()

        return redirect('review_details')

# -----------------------------------------------------------------------------------------------------------------------
