from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import UserKYCDocument, OtherServices
from core.models import UserAccount
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django import forms


class userRegistrationForm(UserCreationForm):

    USER_TYPE_CHOICES = (
        ('Retailer', 'Retailer'),
        ('Distributor', 'Distributor'),
        ('Master Distributor', 'Master Distributor'),
    )

    userType = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='User Type', widget=forms.Select(attrs={'class': 'form-control form-control-lg border-left-0 px-2'}))
    shopName = forms.CharField(label='Shop Name', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off', 'placeholder':'Nitaj Enterprises'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2','autofocus': False, 'autocomplete':'off', 'placeholder':'imjatinx'}))
    pancard_no = forms.CharField(label='Pan Number', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2','autofocus': False, 'autocomplete':'off'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off', 'placeholder':'Jatin'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off', 'placeholder':'Gautam'}))
    mobile = forms.CharField(label='Mobile Number', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off', 'placeholder':'+91 639 506 XXXX'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off', 'placeholder':'jatin.gautam@gmail.com'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg border-left-0 px-2', 'autocomplete':'off'}))
    
    class Meta:
        model = UserAccount
        fields = ['userType','shopName', 'username', 'first_name', 'last_name', 'mobile', 'email', 'password1', 'password2', 'address', 'pancard_no']

class CreateCustomUserForm(UserCreationForm):

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Jatin'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Gautam'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'jatin.gautam@gmail.com'}))
    mobile = forms.CharField(label='Mobile Number', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'+91 639 506 XXXX'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','autofocus': False, 'autocomplete':'off', 'placeholder':'imjatinx'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    shopName = forms.CharField(label='Shop Name', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off', 'placeholder':'Nitaj Enterprises'}))
    pancard_no = forms.CharField(label='Pan Number', widget=forms.TextInput(attrs={'class': 'form-control','autofocus': False, 'autocomplete':'off'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    
    class Meta:
        model = UserAccount
        fields = ['shopName', 'username', 'first_name', 'last_name', 'mobile', 'email', 'password1', 'password2', 'address', 'pancard_no']


class userLoginForm(AuthenticationForm):

    error_messages = {
        'invalid_login': 'Please enter a correct username and password.',
        'inactive': 'This account is inactive.'
        }

    username = forms.CharField(
        label='Username', 
        widget=forms.TextInput(attrs={
            'class': 'input form-control mb20', 
            'autocomplete':"off",
            'style':"height: 40px!important; font-size: 14px !important;"
            }))
    
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={
            'class': 'input form-control mb20',
            'autocomplete':"off",
            'style':"height: 40px!important; font-size: 14px !important;"
            }))


class UserKYCDocumentForm(forms.ModelForm):

    documentComment = forms.CharField(label='Comments', max_length=150, required=False, widget=forms.Textarea(attrs={"rows":"2", 'class':'form-control'}))

    aadharFront = forms.FileField(
        label='Aadhar Front',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )
    
    aadharBack = forms.FileField(
        label='Aadhar Back',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )
    
    pancard = forms.FileField(
        label='Pancard',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )

    cancelChequePassbook = forms.FileField(
        label='Cancel Cheque/Passbook',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )
    
    declarationForm = forms.FileField(
        label='Self Declaration Form',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )

    photo = forms.FileField(
        label='Passport Size Photo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )

    policeVerification = forms.FileField(
        label='Police Verification',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
        ], widget=forms.ClearableFileInput(attrs={"class":"form-control"})
    )

    class Meta:
        model = UserKYCDocument
        fields = ['aadharFront', 'aadharBack', 'pancard', 'documentComment', 'cancelChequePassbook', 'declarationForm', 'photo', 'policeVerification']

    def clean(self):
        cleaned_data = super().clean()

        for field_name in ['aadharFront', 'aadharBack', 'pancard', 'cancelChequePassbook', 'declarationForm', 'photo', 'policeVerification']:
            document_file = cleaned_data.get(field_name)

            if document_file and document_file.size > settings.MAX_UPLOAD_SIZE:
                self.add_error(field_name, 'File size exceeds the limit.')

            if document_file:
                self.validate_file_format(document_file)

        return cleaned_data

    def validate_file_format(self, document_file):
        file_signature = document_file.read(4)
        document_file.seek(0)  # Rewind the file pointer for further processing

        allowed_signatures = {
            b'%PDF': 'PDF',
            b'\xFF\xD8\xFF\xE0': 'JPEG',
            b'\x89PNG': 'PNG',
        }

        for signature, file_type in allowed_signatures.items():
            if file_signature.startswith(signature):
                return  # Valid file type

        raise forms.ValidationError(f'Invalid file format. Only {", ".join(allowed_signatures.values())} are allowed.')
    

# class OtherServicesForm(forms.ModelForm):
#     serviceName = forms.CharField(label='Service Name', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}))
    
#     serviceDescription = forms.CharField(label='Service Description', widget=forms.Textarea(attrs={'rows':5,'class': 'form-control form-control', 'autocomplete':'off'}))

#     class Meta:
#         model = OtherServices
#         fields = ['name', 'gender', 'father_name', 'dob', 'address', 'mobile', 'email', 'adhaar', 'pan', 'doc1', 'doc2', 'doc3', 'doc4', 'serviceDescription', 'serviceName']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
