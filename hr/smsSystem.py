from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from hr.models import JobPost


#applications = candidateApplication.objects.filter(user=request.user) inside views
#Send email to candidate based on HR action (shortlist, select, reject)
def send_hr_action_email(application, action):

    try:
        candidate_user = application.user
        job = application.job

        # Get candidate name
        candidate_name = f"{candidate_user.first_name} {candidate_user.last_name}".strip()
        if not candidate_name:
            candidate_name = candidate_user.username

        # Determine subject and message based on action
        if action == 'shortlisted':
            subject = f"Shortlisted for {job.title} Position – {job.CompanyName}"
            message = f"""Dear {candidate_name},

We are pleased to inform you that your application for the position of "{job.title}" at {job.CompanyName} has been shortlisted.

After reviewing your profile and qualifications, we believe your skills match our requirements, and we would like to move forward to the next stage of the selection process.

Our team will contact you soon with further details regarding the next steps.

Congratulations and best of luck!

Warm regards,
HR Team
{job.CompanyName}"""
            
#####################################################################################

        elif action == 'selected':
            subject = f"Congratulations! You Have Been Selected – {job.title}"
            message = f"""Dear {candidate_name},

Congratulations!

We are delighted to inform you that you have been selected for the position of "{job.title}" at {job.CompanyName}.

Your skills, experience, and performance during the selection process impressed our team.

Further details regarding your joining date, offer letter, and other formalities will be shared with you shortly.

Welcome to the team! We look forward to working with you.

Best wishes,
HR Department
{job.CompanyName}"""
            
#####################################################################################################

        elif action == 'rejected':
            subject = f"Update on Your Application – {job.title}"
            message = f"""Dear {candidate_name},

Thank you for applying for the position of "{job.title}" at {job.CompanyName}.

After careful consideration, we regret to inform you that you have not been selected for this position.

This was a difficult decision due to the high number of qualified applicants.

We truly appreciate your interest in our organization and encourage you to apply again for future opportunities that match your profile.

We wish you all the best in your career journey.

Sincerely,
HR Team
{job.CompanyName}"""
####################
        elif action == 'rejected_after_shortlist':
            subject = f"Update on Your Application – {job.title}"
            message = f"""Dear {candidate_name},

Thank you for participating in our selection process for the position of "{job.title}" at {job.CompanyName}.

We appreciate the time you took to interview with us. After careful review of your profile and our recent interactions, we regret to inform you that we have decided to move forward with other candidates who more closely match our specific needs for this role.

This was a difficult decision, and we were impressed with your qualifications.

We will keep your resume on file for future openings that may be a good fit.

We wish you all the best in your career endeavors.

Sincerely,
HR Team
{job.CompanyName}"""
            
#################################################
        else:
            return  # Invalid action





##############################################

        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[candidate_user.email],
            fail_silently=False,
        )

        print(f"[EMAIL SUCCESS] {action.capitalize()} email sent to {candidate_user.email} for job {job.title}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send {action} email to {candidate_user.email}: {str(e)}")







### Send email to job portal official email when contact form is submitted #################
def send_contact_form_email(name, email, message):

    try:
        subject = f"New Contact Form Submission from {name}"
        
        body = f"""New contact form submission:

Name: {name}
Email: {email}
Message:
{message}

---
This message was sent from the Job Portal contact form."""


        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['hrjobportal.system@gmail.com'],
            fail_silently=False,
        )

        print(f"[EMAIL SUCCESS] Contact form email sent to hrjobportal.system@gmail.com from {email}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send contact form email: {str(e)}")
