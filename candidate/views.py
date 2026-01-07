from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hr.models import JobPost, candidateApplication
from candidate.models import IsShortlisted, CandidateProfile
from candidate.forms import JobApplicationForm, CandidateProfileForm

@login_required(login_url='login_user')
def candidate_dashboard(request):
    """Display candidate dashboard with sidebar navigation"""
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        profile = None
    
    # Get all available jobs
    jobs = JobPost.objects.all().order_by('-created_at')
    applied_jobs = candidateApplication.objects.filter(user=request.user)
    applied_job_ids = [app.job.id for app in applied_jobs]
    
    # Create a dictionary mapping job_id to application status
    job_status_map = {app.job.id: app.status for app in applied_jobs}
    
    # Annotate each job with its application status
    for job in jobs:
        if job.id in job_status_map:
            job.application_status = job_status_map[job.id]
        else:
            job.application_status = None
    
    shortlisted_jobs = IsShortlisted.objects.filter(user=request.user)
    shortlisted_count = shortlisted_jobs.count()
    
    unread_shortlist = shortlisted_jobs.filter(notification_read=False)
    for shortlist in unread_shortlist:
        messages.success(request, f"Congratulations! You have been shortlisted for {shortlist.job.title}!")
        shortlist.notification_read = True
        shortlist.save()
    
    context = {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'shortlisted_count': shortlisted_count,
        'profile': profile,
    }
    return render(request, 'candidate/dashboard_with_nav.html', context)

@login_required(login_url='login_user')
def job_detail(request, pk):
    job = JobPost.objects.get(id=pk)
    application = candidateApplication.objects.filter(user=request.user, job=job).first()
    has_applied = application is not None
    application_status = application.status if application else None
    is_shortlisted = IsShortlisted.objects.filter(user=request.user, job=job).exists()
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            
            job.applycount += 1
            job.save()
            
            messages.success(request, "Application submitted successfully!")
            return redirect('candidate_dashboard')
        # Form errors will now be displayed directly in the template
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'application_status': application_status, # Pass application status to template
        'is_shortlisted': is_shortlisted,
        'form': form,
    }
    return render(request, 'candidate/job_detail.html', context)

@login_required(login_url='login_user')
def shortlisted_jobs(request):
    """Display jobs where candidate has been shortlisted"""
    shortlisted = IsShortlisted.objects.filter(user=request.user).order_by('-shortlisted_date')
    
    context = {
        'shortlisted_jobs': shortlisted,
        'count': shortlisted.count(),
    }
    return render(request, 'candidate/shortlisted.html', context)

@login_required(login_url='login_user')
def candidate_profile(request):
    """Display candidate profile creation/editing page"""
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('candidate_profile')
    else:
        form = CandidateProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'candidate/profile.html', context)

# The original candidate_dashboard_with_nav function is now redundant and can be removed
