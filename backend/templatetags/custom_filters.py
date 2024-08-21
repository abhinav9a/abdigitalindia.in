from django import template
from backend.models import UserAccount
from datetime import datetime


register = template.Library() 

@register.filter(name='get_user_by_id') 
def get_user_by_id(id):
    return UserAccount.objects.get(id=id)

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='truncate_string')
def truncate_string(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '..'
    return value

@register.filter(name="format_date")
def format_date(date_str):
    try:
        # Parse the date in DD/MM format
        date_obj = datetime.strptime(date_str, '%d/%m')
        # Format the date in DD-MMM format
        return date_obj.strftime('%d-%b').title()
    except ValueError:
        return date_str