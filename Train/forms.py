from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User

class Registration_Form(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Confirm Password'}), required=False)
    
    def __init__(self, *args, **kwargs):
        super(Registration_Form, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields.get('username').required = False
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email',
        }

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}),
            'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First Name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last Name'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'}),
        }

    def clean_username(self):
        inp_username = self.cleaned_data.get('username')
        if len(inp_username) == 0:
            raise ValidationError(_("Please Enter Username!!"))
        return inp_username

    def clean_first_name(self):
        inp_first_name = self.cleaned_data.get('first_name')
        if len(inp_first_name) == 0:
            raise ValidationError(_("Please Enter First Name!!"))
        return inp_first_name

    def clean_last_name(self):
        inp_last_name = self.cleaned_data.get('last_name')
        if len(inp_last_name) == 0:
            raise ValidationError(_("Please Enter Last Name!!"))
        return inp_last_name

    def clean_email(self):
        inp_email = self.cleaned_data.get('email')
        if len(inp_email) == 0:
            raise ValidationError(_("Please Enter Email!!"))
        validator = EmailValidator(_("Please Enter Valid Email!!")) 
        validator(inp_email)
        if User.objects.filter(email=inp_email, is_active=True).exists():
            raise ValidationError(_(f"{inp_email} Already Exists!!"))
        return inp_email

    def clean_password1(self):
        inp_password1 = self.cleaned_data.get('password1')
        if len(inp_password1) == 0:
            raise ValidationError(_("Please Enter Password!!"))
        return inp_password1

    def clean_password2(self):
        inp_password1 = self.data.get('password1')
        inp_password2 = self.cleaned_data.get('password2')
        if len(inp_password2) == 0:
            raise ValidationError(_("Please Confirm Your Password!!"))
        if inp_password1 != inp_password2:
            raise ValidationError(_("Password and Confirm Password Must Matched!!"))
        return inp_password2

class Login_Form(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class' : 'form-control text-dark', 'placeholder' : 'Username'}), required=False)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class' : 'form-control text-dark', 'placeholder' : "Password"}),required=False
    )
    
    def clean_username(self):
        inp_username = self.cleaned_data.get('username')
        if len(inp_username) == 0:
            raise ValidationError(_("Please Enter Username!!"))
        return inp_username

    def clean_password(self):
        inp_password = self.cleaned_data.get('password')
        if len(inp_password) == 0:
            raise ValidationError(_("Please Enter Password!!"))
        return inp_password

class Status_Form(forms.Form):
    train_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Train PNR No.'}), required=False)
    date = forms.DateField(help_text="YYYY-MM-DD", widget=forms.DateInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Date'}), required=False)

    def clean_train_number(self):
        inp_train_number = self.cleaned_data.get("train_number")
        if len(inp_train_number) == 0:
            raise ValidationError(_("Please Enter Valid Train Number!!"))
        return inp_train_number

    def clean_date(self):
        inp_date = self.cleaned_data.get("date")
        if inp_date == None:
            raise ValidationError(_("Please Enter Valid Date!!"))
        return inp_date

class Enquiry_Form(forms.Form):
    from_station = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Source Station Code'}), required=False)
    to_station = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Destination Station Code'}), required=False)

    def clean_from_station(self):
        inp_from_station = self.cleaned_data.get("from_station")
        if len(inp_from_station) == 0:
            raise ValidationError(_("Please Enter Valid Station Code!!"))
        return inp_from_station

    def clean_to_station(self):
        inp_to_station = self.cleaned_data.get("to_station")
        if len(inp_to_station) == 0:
            raise ValidationError(_("Please Enter Valid Station Code!!"))
        return inp_to_station

class Pnr_Form(forms.Form):
    pnr = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '10 Digit PNR no.'}), required=False)

    def clean_pnr(self):
        inp_pnr = self.cleaned_data.get("pnr")
        if len(inp_pnr) == 0 or len(inp_pnr) > 10:
            raise ValidationError(_("Please Enter Valid PNR No.!!"))
        return inp_pnr