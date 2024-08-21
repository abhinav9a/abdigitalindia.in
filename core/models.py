from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
import os

def document_file_path(instance, filename):
    base_path = 'media/ProfileImg'
    username = instance.username
    timestamp_now = timezone.now().strftime('%Y%m%d%H%M%S')
    cleaned_filename = f"{slugify(os.path.splitext(filename)[0])}_{timestamp_now}{os.path.splitext(filename)[1]}"
    user_folder = os.path.join(base_path, username)
    return os.path.join(user_folder, cleaned_filename)

class UserAccount(AbstractUser):
    """
    Customizing the User model
    """

    class KycStatus(models.TextChoices):
        Pending = "P", _("Pending")
        Complete = "C", _("Complete")
        Rejected = "R", _("Rejected")
        
    userType = models.CharField(_("User Type"), max_length=50)
    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True)
    shopName = models.CharField(_("Shop Name"), max_length=100)
    address = models.CharField(_("Address"), max_length=100)
    mobile = models.CharField(_("Mobile"), max_length=10)
    kycStatus = models.CharField(max_length=20, choices=KycStatus.choices, default=KycStatus.Pending)
    pancard_no = models.CharField(_('PanCard Number') ,max_length=20, null=True, blank=True)
    userManager = models.CharField(_("User Manager"), max_length=120, null=True, blank=True)
    platform_id = models.CharField(_("Platform id"), unique=True, max_length=500, null=True, blank=True)
    eko_user_code = models.CharField(_("Eko User Code"), max_length=500, null=True, blank=True)
    pay_sprint_ref_no = models.CharField(_("PaySprint Ref Number"), max_length=500, null=True, blank=True)

    dob = models.DateField(_("Date of Birth"), null=True, blank=True)
    unique_sequence = models.IntegerField(_("Unique sequence"), null=True, blank=True, default=1)

    acc_name = models.CharField(_("Account Name"), max_length=500, blank=True)
    acc_no = models.CharField(_("Account Number"), max_length=500, blank=True)
    acc_type = models.CharField(_("Account Type"), max_length=500, blank=True)
    ifsc = models.CharField(_("IFSC"), max_length=500, blank=True)
    payment_mode = models.CharField(_("Payment Mode"), max_length=500, blank=True)

    profile_img = models.ImageField(_("Profile Photo"), upload_to=document_file_path, blank=True)

    def formatted_series(self):
        # Format the series field with leading zeros and a total length of 4 characters
        return "{:04d}".format(self.unique_sequence)


class ContactForm(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    subject = models.CharField(_("Subject"), max_length=50)
    message = models.TextField(_("Message"))

    def __str__(self):
        return self.name

