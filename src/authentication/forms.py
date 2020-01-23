from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """
        Form for creating new users
        Includes the required fields (username, email) 
        plus a repeated password
    """

    password1 = forms.CharField()
    password2 = forms.CharField()


    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        """
            Check whether user with provided username exists
        """
        print('clean_username')
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("Cannot use this username. It's already registered")
        return username

    def clean_email(self):
        """
            Check whether user with provided email exists
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered")
        return email

    def clean_password2(self):
        """
            Check that the two password entries match
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
            Save the provided hashed password
        """
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
            # user.profile.send_activation_email()
        return user
