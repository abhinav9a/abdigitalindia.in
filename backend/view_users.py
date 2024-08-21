from django.shortcuts import render, redirect
from .forms import userRegistrationForm, userLoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from core.models import UserAccount
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import generate_platform_id
from django.contrib.auth import update_session_auth_hash
from .forms import UserPasswordChangeForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from PIL import Image


def user_signup(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            username = form.cleaned_data.get('username').lower()
            pancard_no = form.cleaned_data.get('pancard_no').upper()
            newUser.username = username
            newUser.pancard_no = pancard_no.upper()
            newUser.userManager = 1
            newUser.is_active = True

            serial_number, platform_id = generate_platform_id(newUser.userType)       
            newUser.unique_sequence = serial_number
            newUser.platform_id = platform_id

            newUser.save()

            defaultGroup = Group.objects.filter(name=newUser.userType).first()
            newUser.groups.add(defaultGroup)

            return redirect('user_login')
    else:
        form = userRegistrationForm()
    return render(request, 'backend/User/UserSignup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = userLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            redirect('user_login')
    else:
        form = userLoginForm()
    return render(request, 'backend/User/UserLogin.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def user_profile(request):
    userProfile = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        try:
            dob = request.POST.get('dob')
            profile_img = request.FILES['profile_img']
            userProfile.dob = dob
            userProfile.profile_img = profile_img
            userProfile.save()
            messages.success(request, message='Profile update successfully',extra_tags='success')
        except Exception as e:
            messages.error(request, message=e, extra_tags='danger')

        
        return redirect('user_profile')

    return render(request, 'backend/User/UserProfile.html', {'userProfile':userProfile, 'dob':str(userProfile.dob)})

@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill valid details.')
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'backend/User/UserChangePassword.html', {'form': form})

@login_required(login_url='user_login')
def generate_id_card(request):
    user_instance = UserAccount.objects.get(username=request.user)
    
    # Generate PDF using existing template
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user_instance.username}_Certificate.pdf"'

    # Load image as template
    image_path = 'static/backendAssets/certificate1.jpg'
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    # Create canvas for drawing on PDF
    p = canvas.Canvas(response, pagesize=(img_width, img_height))
    
    # Draw image template on canvas
    p.drawImage(image_path, 0, 0, width=img_width, height=img_height)

    last_name = user_instance.last_name if user_instance.last_name else '.'
    
    # Draw user details on the PDF
    p.setFont("Helvetica-Bold", 34)
    p.drawString(500, 545, f'{user_instance.userType}')
    p.drawString(480, 465, f'{user_instance.first_name} {last_name}')
    p.drawString(380, 385, f'{user_instance.address}')
    p.setFont("Helvetica-Bold", 28)
    p.drawString(230, 305, f'{user_instance.platform_id}')
    p.drawString(920, 305, f'{user_instance.pancard_no}')
    p.drawString(130, 226, f'{user_instance.date_joined.date()}')
    
    if user_instance.profile_img:
        profile_img_path = user_instance.profile_img
        profile_img = ImageReader(profile_img_path)
        p.drawImage(profile_img, 1030, 660, width=150, height=170)

    p.save()

    return response


