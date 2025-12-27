from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hr.models import candidateApplication, EDUCATION_CHOICES


class CandidateRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    cpassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }), label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        cpassword = cleaned_data.get('cpassword')
        
        if password and cpassword:
            if password != cpassword:
                raise ValidationError("Passwords do not match")
        
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = candidateApplication
        fields = ['education_level', 'passingYear', 'yearOfExp', 'resume', 'support_documents']
        widgets = {
            'education_level': forms.Select(attrs={
                'class': 'form-control',
            }),
            'passingYear': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year of passing (e.g., 2023)',
            }),
            'yearOfExp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience',
                'min': '0',
                'step': '1',
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
            }),
            'support_documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
            }),
        }
        labels = {
            'education_level': 'Highest Education Level',
            'passingYear': 'Passing Year',
            'yearOfExp': 'Years of Experience',
            'resume': 'CV/Resume (PDF, max 5MB)',
            'support_documents': 'Supporting Documents (Optional - PDF, max 5MB)',
        }
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are accepted for resume/CV.")
            if resume.size > 5242880:  # 5MB = 5242880 bytes
                raise ValidationError("Resume file size must not exceed 5MB.")
        return resume
    
    def clean_support_documents(self):
        support_docs = self.cleaned_data.get('support_documents')
        if support_docs:
            if not support_docs.name.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are accepted for supporting documents.")
            if support_docs.size > 5242880:  # 5MB
                raise ValidationError("Supporting documents file size must not exceed 5MB.")
        return support_docs
    
    def clean_yearOfExp(self):
        years = self.cleaned_data.get('yearOfExp')
        if years is not None:
            if years < 0:
                raise ValidationError("Years of experience cannot be negative. Minimum is 0.")
        return years
    
    def clean_passingYear(self):
        year = self.cleaned_data.get('passingYear')
        from datetime import datetime
        current_year = datetime.now().year
        if year:
            if year > current_year:
                raise ValidationError("Passing year cannot be in the future.")
            if year < 1990:
                raise ValidationError("Passing year seems too old. Please verify.")
        return year
