from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    # Potrebno za generisanje slika usluga na pocetnoj strani
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_range'] = range(1, 48)
        context['services'] = Service.objects.all()

        return context

#-----------------------------------------------------------------------------------------------------------------------
def error_404(request, exception):
    return render(request, '404.html', {'is_404': True}, status=404)

#-----------------------------------------------------------------------------------------------------------------------
def error_500(request):
    return render(request, '500.html', {'is_500': True}, status=500)

#-----------------------------------------------------------------------------------------------------------------------
