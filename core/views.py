from django.shortcuts import render
from django.http import JsonResponse
from .forms import WebsiteContactForm
from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = WebsiteContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success':True, 'message': "We've received your request."})
        else:
            return JsonResponse({'success':False, 'form_error':form.errors, 'message': 'Please enter correct details'})
    else:
        form = WebsiteContactForm()
    return render(request, 'core/Pages/home.html', {'form':form})

def termsAndConditions(request):
    return render(request, 'core/Pages/termsAndConditions.html')

def privacyPolicy(request):
    return render(request, 'core/Pages/privacyPolicy.html')

def refundCancellation(request):
    return render(request, 'core/Pages/refundCancellation.html')
