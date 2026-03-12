from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from grooming_salon.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from grooming_salon.accounts.models import Profile, EmailVerificationToken
from grooming_salon.utils.mixins import UserOwnedModelMixin, ImageCleanupMixin, RedirectIfAuthenticatedMixin

UserModel = get_user_model()

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class AppUserRegisterView(RedirectIfAuthenticatedMixin, CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            mark_safe('Registracija je uspešna!<br>Poslali smo link<br>za verifikaciju na e-mail.<br> '
                      'Klikni na link da aktiviraš nalog.<br>'
                      '(proveri spam folder)')
        )
        return response
#-----------------------------------------------------------------------------------------------------------------------
class AppUserLoginView(RedirectIfAuthenticatedMixin, LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'

#-----------------------------------------------------------------------------------------------------------------------
class AppUserLogoutView(LogoutView):
    pass

#-----------------------------------------------------------------------------------------------------------------------
class AppUserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change-page.html'
    success_url = reverse_lazy('profile_details')

    def form_valid(self, form):
        messages.success(self.request, 'Lozinka je uspešno promenjena!')
        return super().form_valid(form)

class ProfileEditView(LoginRequiredMixin, PermissionRequiredMixin, UserOwnedModelMixin, ImageCleanupMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'
    success_url = reverse_lazy('profile_details')
    permission_required = 'accounts.change_profile'

    # UserOwned Mixin nam dobavlja filtriran queryset za ulogovanog korisnika
    def get_object(self, queryset=None):
        return self.get_queryset().get()

    # ImageCleanup Mixin validira da li je slika obrisana kada korisnik aktivira (X)
    def form_valid(self, form):
        if self.handle_image_cleanup(form):
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

#-----------------------------------------------------------------------------------------------------------------------
class AppUserDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserOwnedModelMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    permission_required = 'accounts.view_profile'

    # UserOwned Mixin nam dobavlja filtriran queryset za ulogovanog korisnika
    def get_object(self, queryset=None):
        return self.get_queryset().get()

    # Dovlačimo podatke o psima preko related_name 'dogs'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dogs'] = self.object.dogs.all()
        return context

#-----------------------------------------------------------------------------------------------------------------------
class AppUserDeleteView(LoginRequiredMixin, UserOwnedModelMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    # UserOwned Mixin nam dobavlja filtriran queryset za ulogovanog korisnika
    def get_object(self, queryset=None):
        return self.get_queryset().get()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        return redirect(self.get_success_url())

#-----------------------------------------------------------------------------------------------------------------------
def verify_email(request, token):
    try:
        verification = EmailVerificationToken.objects.select_related('user').get(token=token)

        if verification.is_expired():
            verification.delete()
            messages.warning(request, mark_safe('Link je istekao.<br>Registrujte se ponovo.'))
            return redirect('register')

        user = verification.user
        user.is_active = True
        user.save()

        # Brišemo token - više nije potreban
        verification.delete()

        messages.success(request, mark_safe('E-mail je potvrđen!<br>Možete se prijaviti.'))
        return redirect('login')

    except EmailVerificationToken.DoesNotExist:
        messages.error(request, mark_safe('Nevažeći verifikacioni link.'))
        return redirect('register')

#-----------------------------------------------------------------------------------------------------------------------
