from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.forms import extras
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode
try:
    from django.contrib.sites.models import get_current_site
except ImportError:
    from django.contrib.sites.shortcuts import get_current_site

from ckeditorfiles.widgets import CKEditorWidget

# -----------------------------------------------------------------------------
# -- Admin/Registration Account Maintenance Forms
# -----------------------------------------------------------------------------

class UserChangeForm(forms.ModelForm):
   
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
    is_superuser = forms.BooleanField(required=False, label=_('User is a Super User'),
        help_text=_("User can access all areas of the CMS without having to "
        "have permissions assigned."))

    about = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['user_about_ckeditor']), required=False)


    
    class Meta:
        model = get_user_model()

        fields = ['first_name','last_name','email','password','is_superuser']

    def clean_password(self):
        return self.initial["password"]

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        return self.cleaned_data["email"].lower()




class UserCreationForm(forms.ModelForm):
    
    
    first_name = forms.CharField(label=_("First Name"), required=True)
    last_name = forms.CharField(label=_("Last Name"), required=True)
    email = forms.RegexField(label=_("Email"), max_length=75,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. Letters, digits and @/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")
        }
    )
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}),
        help_text=_("Enter the same password as above, for verification."))


    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email']

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.cleaned_data["username"] = self.cleaned_data["email"] = email.lower()

        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email.lower()
        raise forms.ValidationError(settings.MESSAGES['error_duplicate_email'])

    def clean_username(self):
        return self.clean_email()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError( settings.MESSAGES['error_password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



# class PasswordResetForm(BasePasswordResetForm):
    
#     def save(self, domain_override=None,
#              subject_template_name='registration/password_reset_subject.txt',
#              email_template_name='registration/password_reset_email.html',
#              use_https=False, token_generator=default_token_generator,
#              from_email=None, request=None):
#         """
#         Generates a one-use only link for resetting password and sends to the
#         user.
#         """
#         UserModel = get_user_model()
        
#         email = self.cleaned_data["email"]
#         active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)
#         for user in active_users:
            
#             # Make sure that no email is sent to a user that actually has
#             # a password marked as unusable
#             if not user.has_usable_password():
#                 continue
            
#             if not domain_override:
#                 current_site = get_current_site(request)
#                 site = current_site
#                 domain = current_site.domain
#             else:
#                 site_name = domain = domain_override
#             c = {
#                 'email': user.email,
#                 'domain': domain,
#                 'site': site,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'user': user,
#                 'token': token_generator.make_token(user),
#                 'protocol': 'https' if use_https else 'http',
#             }
#             user.send_password_reset(c)


# class CustomAuthentication(AuthenticationForm):
#     pass
    
    


# class CreateAccountForm(RegistrationFormUniqueEmail):
    
#     first_name = forms.CharField(label=_("First Name"), required=True)
#     last_name = forms.CharField(label=_("Last Name"), required=True)

    
#     next = forms.CharField(required=False)


#     def __init__(self, *args, **kwargs): 
#         super(CreateAccountForm, self).__init__(*args, **kwargs) 
        
#         self.fields.pop('username')


#     def clean_email(self):
#         """
#         Validate that the supplied email address is unique for the
#         site.
        
#         """
#         email = self.cleaned_data["email"]
#         self.cleaned_data["username"] = self.cleaned_data["email"] = email.lower()

#         if get_user_model().objects.filter(email__iexact=self.cleaned_data['email']):
#             raise forms.ValidationError(_(settings.MESSAGES['error_duplicate_email']))
#         return self.cleaned_data['email']
   


class UserGroupAdminForm(forms.ModelForm):
   
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['usergroup_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['usergroup_synopsis_ckeditor']), required=False)
