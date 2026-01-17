from django import forms
from hr.models import JobPost, candidateApplication, EDUCATION_CHOICES, HRProfile
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'address', 'CompanyName', 'salaryLow', 'salaryHigh', 'lastDateToApply']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Location'
            }),
            'CompanyName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'salaryLow': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum Salary',
                'min': '0',
                'step': '1'
            }),
            'salaryHigh': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum Salary',
                'min': '0',
                'step': '1'
            }),
            'lastDateToApply': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salary_low = cleaned_data.get('salaryLow')
        salary_high = cleaned_data.get('salaryHigh')
        last_date = cleaned_data.get('lastDateToApply')
        
        if salary_low is not None and salary_low < 0:
            self.add_error('salaryLow', "Salary cannot be negative. Minimum value is 0.")
        
        if salary_high is not None and salary_high < 0:
            self.add_error('salaryHigh', "Salary cannot be negative. Minimum value is 0.")
        
        if salary_low is not None and salary_high is not None:
            if salary_low > 0 and salary_high > 0 and salary_low >= salary_high:
                raise ValidationError("Maximum salary must be greater than minimum salary")
        
        if last_date:
            today = date.today()
            if last_date <= today:
                raise ValidationError("Last date to apply must be after today. You cannot select today or any past date.")
        
        return cleaned_data


class CandidateApplicationForm(forms.ModelForm):
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
                'step': '1'
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
        if years is not None and years < 0:
            raise ValidationError("Years of experience cannot be negative. Minimum value is 0.")
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


class HRProfileForm(forms.ModelForm):
    class Meta:
        model = HRProfile
        fields = [
            'company_name', 'company_logo', 'cover_image', 'industry', 'company_type',
            'employee_size', 'email', 'phone_number', 'website', 'location',
            'about_company', 'linkedin_url', 'facebook_url', 'twitter_url', 'instagram_url'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name',
            }),
            'company_logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'industry': forms.Select(attrs={
                'class': 'form-control',
            }),
            'company_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'employee_size': forms.Select(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company email',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company location',
            }),
            'about_company': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your company...',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/company/...',
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/...',
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/...',
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/...',
            }),
        }
        labels = {
            'company_name': 'Company Name',
            'company_logo': 'Company Logo',
            'cover_image': 'Cover Image',
            'industry': 'Industry',
            'company_type': 'Company Type',
            'employee_size': 'Employee Size',
            'email': 'Company Email',
            'phone_number': 'Phone Number',
            'website': 'Website',
            'location': 'Location',
            'about_company': 'About Company',
            'linkedin_url': 'LinkedIn',
            'facebook_url': 'Facebook',
            'twitter_url': 'Twitter',
            'instagram_url': 'Instagram',
        }
    
    def clean_company_logo(self):
        logo = self.cleaned_data.get('company_logo')
        if logo:
            if logo.size > 5242880:  # 5MB
                raise ValidationError("Logo size must not exceed 5MB.")
            if not logo.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError("Only image files (JPG, PNG, GIF) are accepted.")
        return logo
    
    def clean_cover_image(self):
        cover = self.cleaned_data.get('cover_image')
        if cover:
            if cover.size > 5242880:  # 5MB
                raise ValidationError("Cover image size must not exceed 5MB.")
            if not cover.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError("Only image files (JPG, PNG, GIF) are accepted.")
        return cover
