from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hr.models import candidateApplication, EDUCATION_CHOICES
from candidate.models import CandidateProfile


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
            'passingYear': forms.Select(attrs={
                'class': 'form-control',
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
            'passingYear': 'Graduation Year',  # Renamed from "Passing Year" to "Graduation Year"
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
        
        if year and year != 'currently_running':
            from datetime import datetime
            current_year = datetime.now().year
            try:
                year_int = int(year)
                if year_int > current_year:
                    raise ValidationError(f"Passing year cannot be in the future. Current year is {current_year}.")
                if year_int < 1990:
                    raise ValidationError("Passing year cannot be before 1990.")
            except ValueError:
                raise ValidationError("Invalid year format.")
        
        return year


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = [
            'profile_photo',
            'job_preference_title',
            'preferred_job_level',
            'preferred_job_type',
            'work_experience',
            'education_level',
            'course_or_program',
            'gpa_percentage_type',
            'gpa_percentage_value',
            'school_college_name',
            'graduation_year',
            'skills',
            'languages',
            'social_account_name_1',
            'social_account_url_1',
            'social_account_name_2',
            'social_account_url_2',
        ]
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'job_preference_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Document Officer',
            }),
            'preferred_job_level': forms.Select(attrs={
                'class': 'form-control',
            }),
            'preferred_job_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'work_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
                'placeholder': 'Years of experience',
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-control',
            }),
            'course_or_program': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., BIM',
            }),
            'gpa_percentage_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'gpa_percentage_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter your GPA or Percentage',
            }),
            'school_college_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of school/college/institute',
            }),
            'graduation_year': forms.Select(attrs={
                'class': 'form-control',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Public Speaking, Computer Operation',
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Nepali, English',
            }),
            'social_account_name_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Facebook',
            }),
            'social_account_url_1': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'social_account_name_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., LinkedIn',
            }),
            'social_account_url_2': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
        }
        labels = {
            'profile_photo': 'Profile Photo (Passport size)',
            'job_preference_title': 'Job Preference Title',
            'preferred_job_level': 'Preferred Job Level',
            'preferred_job_type': 'Preferred Job Type',
            'work_experience': 'Work Experience (Years)',
            'education_level': 'Education Level',
            'course_or_program': 'Course or Program',
            'gpa_percentage_type': 'GPA or Percentage',
            'gpa_percentage_value': 'GPA/Percentage Value',
            'school_college_name': 'School/College/Institute Name',
            'graduation_year': 'Graduation Year',
            'skills': 'Skills',
            'languages': 'Languages',
            'social_account_name_1': 'Social Account Name 1',
            'social_account_url_1': 'Social Account URL 1',
            'social_account_name_2': 'Social Account Name 2',
            'social_account_url_2': 'Social Account URL 2',
        }
    
    def clean_work_experience(self):
        experience = self.cleaned_data.get('work_experience')
        if experience is not None:
            if experience < 0:
                raise ValidationError("Work experience cannot be negative.")
        return experience
    
    def clean_gpa_percentage_value(self):
        value = self.cleaned_data.get('gpa_percentage_value')
        gpa_type = self.cleaned_data.get('gpa_percentage_type')
        
        if value is not None:
            if value < 0:
                raise ValidationError("GPA/Percentage cannot be negative. Minimum value is 0.")
            
            if gpa_type == 'gpa_4':
                if value > 4:
                    raise ValidationError("GPA (out of 4) cannot exceed 4.0.")
            elif gpa_type == 'gpa_10':
                if value > 10:
                    raise ValidationError("GPA (out of 10) cannot exceed 10.0.")
            elif gpa_type == 'percentage':
                if value > 100:
                    raise ValidationError("Percentage cannot exceed 100%.")
        
        return value
    
    def clean_graduation_year(self):
        year = self.cleaned_data.get('graduation_year')
        
        if year and year != 'currently_running':
            from datetime import datetime
            current_year = datetime.now().year
            try:
                year_int = int(year)
                if year_int > current_year:
                    raise ValidationError(f"Graduation year cannot be in the future. Current year is {current_year}.")
                if year_int < 1900:
                    raise ValidationError("Graduation year cannot be before 1900.")
            except ValueError:
                raise ValidationError("Invalid year format.")
        
        return year
    
    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5242880:  # 5MB
                raise ValidationError("Profile photo size must not exceed 5MB.")
            if not photo.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError("Only image files (JPG, PNG, GIF) are accepted.")
        return photo
