import json

from django.shortcuts import render, redirect
from .forms import UserKYCDocumentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserKYCDocument
from django.db import IntegrityError
from backend.utils import decrypt_pay_sprint_token_token
from backend.models import UserAccount
import logging


logger = logging.getLogger(__name__)


@login_required(login_url='user_login')
def dashboard(request):
    if 'data' in request.GET:
        jwt_encrypted_data = request.GET['data']
        data = decrypt_pay_sprint_token_token(jwt_encrypted_data)
        logger.error(f"PaySprint Data: {json.dumps(data)}")
        if data is not None and data['status'] == "1":
            onboarding_details = UserAccount.objects.get(username=request.user)
            ref_no = data['refno']
            onboarding_details.pay_sprint_ref_no = ref_no
            onboarding_details.save()
            messages.success(request, message="Merchant Onboarded.", extra_tags='success')
        return redirect("dashboard")

    return render(request, 'backend/Pages/dashboard.html')


# Pending : Path setup for django admin dashboard
@login_required(login_url='user_login')
def kycAction(request):
    documentList = UserKYCDocument.objects.filter(userAccount=request.user)
    if request.method == 'POST':
        form = UserKYCDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a document of the same type already exists for the user
            existing_document = UserKYCDocument.objects.filter(userAccount=request.user).first()

            if existing_document:
                # Display error message if a document of the same type already exists
                messages.error(request, f'You have already uploaded documents.')
            else:
                # Save the form data if no existing document of the same type
                obj = form.save(commit=False)
                obj.userAccount = request.user
                obj.save()

                # Display success message
                messages.success(request, f"Uploaded Successfully. We'll get back to you.")

                # Redirect to the dashboard
                return redirect('dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form and try again.')
    else:
        form = UserKYCDocumentForm()
    return render(request, 'backend/Pages/kycAction.html', {'form': form, 'documentList': documentList})


@login_required(login_url='user_login')
def support(request):
    return render(request, 'backend/Pages/support.html')


@login_required(login_url='user_login')
def unauthorized(request):
    return render(request, 'backend/Pages/Unauthorized.html')

def handler404(request, exception):
    return render(request, 'backend/Pages/404.html', status=404)