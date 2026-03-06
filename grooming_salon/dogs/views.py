from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from grooming_salon.dogs.forms import DogForm, DogDeleteForm
from grooming_salon.dogs.models import Dog
from grooming_salon.utils.mixins import ImageCleanupMixin, UserOwnedModelMixin

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class AddDogView(LoginRequiredMixin, PermissionRequiredMixin, ImageCleanupMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog-add-page.html'
    permission_required = 'dogs.add_dog'


    def form_valid(self, form):
        # Osiguravamo da samo trenutni korisnik može dodati psa
        form.instance.user = self.request.user

        # ImageCleanup Mixin validira da li je slika obrisana kada korisnik aktivira (X)
        if self.handle_image_cleanup(form):
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_details')

#-----------------------------------------------------------------------------------------------------------------------
class DogDetailsView(LoginRequiredMixin, PermissionRequiredMixin, UserOwnedModelMixin, DetailView):
    model = Dog
    template_name = 'dogs/dog-details-page.html'
    context_object_name = 'dog'
    slug_url_kwarg = 'dog_slug'
    permission_required = 'dogs.view_dog'

#-----------------------------------------------------------------------------------------------------------------------
class EditDogView(LoginRequiredMixin, PermissionRequiredMixin, UserOwnedModelMixin, ImageCleanupMixin, UpdateView):
    model = Dog
    form_class = DogForm
    slug_url_kwarg = 'dog_slug'
    context_object_name = 'dog'
    template_name = 'dogs/dog-edit-page.html'
    permission_required = 'dogs.change_dog'

    def form_valid(self, form):
        # ImageCleanup Mixin validira da li je slika obrisana kada korisnik aktivira (X)
        if self.handle_image_cleanup(form):
            return HttpResponseRedirect(self.get_success_url())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dog_details', kwargs={'dog_slug': self.kwargs['dog_slug']})

#-----------------------------------------------------------------------------------------------------------------------
class DeleteDogView(LoginRequiredMixin, PermissionRequiredMixin, UserOwnedModelMixin, DeleteView):
    model = Dog
    template_name = 'dogs/dog-delete-page.html'
    slug_field = 'slug'
    slug_url_kwarg = 'dog_slug'
    context_object_name = 'dog'
    permission_required = 'dogs.delete_dog'

    def get_success_url(self):
        return reverse_lazy('profile_details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DogDeleteForm(initial=self.object.__dict__)
        return context

#-----------------------------------------------------------------------------------------------------------------------
