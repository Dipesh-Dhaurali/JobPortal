from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from functools import wraps
from hr.models import hr, JobPost, HRProfile
from candidate.models import CandidateProfile
from .models import AdminUser, UserStatus, JobPostModeration, AdminActivityLog

# Decorator to check if user is admin
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            admin_user = AdminUser.objects.get(user=request.user)
            return view_func(request, *args, **kwargs)
        except AdminUser.DoesNotExist:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('login_user')
    return wrapper


@login_required(login_url='login_user')
@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics and overview"""
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        messages.error(request, 'Admin access denied.')
        return redirect('login_user')
    
    # Get statistics
    total_users = User.objects.count()
    total_hr = hr.objects.count()
    total_candidates = User.objects.exclude(hr__isnull=False).count()
    total_jobs = JobPost.objects.count()
    total_applications = 0
    
    # Count applications from candidateApplication model
    from hr.models import candidateApplication
    total_applications = candidateApplication.objects.count()
    
    # Get user status breakdown
    active_users = UserStatus.objects.filter(status='active').count()
    suspended_users = UserStatus.objects.filter(status='suspended').count()
    pending_users = UserStatus.objects.filter(status='pending').count()
    
    # Get recent activity
    recent_jobs = JobPost.objects.order_by('-created_at')[:5]
    recent_activity = AdminActivityLog.objects.order_by('-created_at')[:10]
    
    # Get job moderation pending
    pending_moderation = JobPostModeration.objects.filter(status='flagged').count()
    
    context = {
        'total_users': total_users,
        'total_hr': total_hr,
        'total_candidates': total_candidates,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'pending_users': pending_users,
        'recent_jobs': recent_jobs,
        'recent_activity': recent_activity,
        'pending_moderation': pending_moderation,
    }
    
    return render(request, 'admin_portal/dashboard.html', context)


@login_required(login_url='login_user')
@admin_required
def manage_users(request):
    """View and manage all users (HR and Candidates)"""
    try:
        AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    # Get filter parameter
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    users = User.objects.all()
    
    # Apply filters
    if filter_type == 'hr':
        users = users.filter(hr__isnull=False)
    elif filter_type == 'candidate':
        users = users.filter(hr__isnull=True)
    
    # Apply search
    if search_query:
        users = users.filter(username__icontains=search_query) | users.filter(email__icontains=search_query)
    
    users = users.order_by('-date_joined')
    
    # Get status for each user
    user_data = []
    for user in users:
        try:
            status = UserStatus.objects.get(user=user)
        except UserStatus.DoesNotExist:
            status = None
        
        user_type = 'HR' if hr.objects.filter(user=user).exists() else 'Candidate'
        user_data.append({
            'user': user,
            'status': status,
            'user_type': user_type,
        })
    
    context = {
        'user_data': user_data,
        'filter_type': filter_type,
        'search_query': search_query,
    }
    
    return render(request, 'admin_portal/manage_users.html', context)


@login_required(login_url='login_user')
@admin_required
def suspend_user(request, user_id):
    """Suspend a user account"""
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided')
        
        # Update or create user status
        user_status, created = UserStatus.objects.get_or_create(user=user)
        user_status.status = 'suspended'
        user_status.reason_for_suspension = reason
        user_status.suspended_at = timezone.now()
        user_status.suspended_by = admin_user
        user_status.save()
        
        # Log activity
        AdminActivityLog.objects.create(
            admin=admin_user,
            action_type='user_suspended',
            description=f'Suspended user {user.username}. Reason: {reason}',
            target_user=user
        )
        
        messages.success(request, f'User {user.username} has been suspended.')
        return redirect('manage_users')
    
    return render(request, 'admin_portal/suspend_user.html', {'user': user})


@login_required(login_url='login_user')
@admin_required
def activate_user(request, user_id):
    """Activate a suspended user account"""
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    user = get_object_or_404(User, id=user_id)
    
    # Update user status
    user_status, created = UserStatus.objects.get_or_create(user=user)
    user_status.status = 'active'
    user_status.reason_for_suspension = None
    user_status.suspended_at = None
    user_status.suspended_by = None
    user_status.save()
    
    # Log activity
    AdminActivityLog.objects.create(
        admin=admin_user,
        action_type='user_activated',
        description=f'Activated user {user.username}',
        target_user=user
    )
    
    messages.success(request, f'User {user.username} has been activated.')
    return redirect('manage_users')


@login_required(login_url='login_user')
@admin_required
def moderate_jobs(request):
    """View and moderate all job posts"""
    try:
        AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    filter_status = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    # Get all jobs
    jobs = JobPost.objects.all().select_related('user')
    
    # Apply search
    if search_query:
        jobs = jobs.filter(title__icontains=search_query) | jobs.filter(CompanyName__icontains=search_query)
    
    jobs = jobs.order_by('-created_at')
    
    # Get moderation status for each job
    job_data = []
    for job in jobs:
        try:
            moderation = JobPostModeration.objects.get(job_post=job)
        except JobPostModeration.DoesNotExist:
            moderation = None
        
        job_data.append({
            'job': job,
            'moderation': moderation,
        })
    
    context = {
        'job_data': job_data,
        'filter_status': filter_status,
        'search_query': search_query,
    }
    
    return render(request, 'admin_portal/moderate_jobs.html', context)


@login_required(login_url='login_user')
@admin_required
def edit_job(request, job_id):
    """Edit a job post as admin"""
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    job = get_object_or_404(JobPost, id=job_id)
    
    if request.method == 'POST':
        job.title = request.POST.get('title', job.title)
        job.address = request.POST.get('address', job.address)
        job.CompanyName = request.POST.get('CompanyName', job.CompanyName)
        job.salaryLow = request.POST.get('salaryLow', job.salaryLow)
        job.salaryHigh = request.POST.get('salaryHigh', job.salaryHigh)
        job.employment_type = request.POST.get('employment_type', job.employment_type)
        job.work_mode = request.POST.get('work_mode', job.work_mode)
        job.save()
        
        # Log activity
        AdminActivityLog.objects.create(
            admin=admin_user,
            action_type='job_edited',
            description=f'Edited job post: {job.title}',
            target_user=job.user
        )
        
        messages.success(request, 'Job post has been updated.')
        return redirect('moderate_jobs')
    
    context = {
        'job': job,
        'EMPLOYMENT_TYPES': [
            ('full-time', 'Full-time'),
            ('part-time', 'Part-time'),
            ('internship', 'Internship'),
            ('contract', 'Contract'),
            ('freelance', 'Freelance'),
        ],
        'WORK_MODES': [
            ('on-site', 'On-site'),
            ('remote', 'Remote'),
            ('hybrid', 'Hybrid'),
        ],
    }
    
    return render(request, 'admin_portal/edit_job.html', context)


@login_required(login_url='login_user')
@admin_required
def delete_job(request, job_id):
    """Delete a job post"""
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    job = get_object_or_404(JobPost, id=job_id)
    
    if request.method == 'POST':
        job_title = job.title
        job_user = job.user
        job.delete()
        
        # Log activity
        AdminActivityLog.objects.create(
            admin=admin_user,
            action_type='job_deleted',
            description=f'Deleted job post: {job_title}',
            target_user=job_user
        )
        
        messages.success(request, 'Job post has been deleted.')
        return redirect('moderate_jobs')
    
    return render(request, 'admin_portal/delete_job.html', {'job': job})


@login_required(login_url='login_user')
@admin_required
def view_hr_profile(request, user_id):
    """View HR/Company profile"""
    try:
        AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    user = get_object_or_404(User, id=user_id)
    
    try:
        hr_profile = HRProfile.objects.get(user=user)
    except HRProfile.DoesNotExist:
        hr_profile = None
    
    hr_user = hr.objects.filter(user=user).first()
    jobs = JobPost.objects.filter(user=user) if hr_user else []
    
    context = {
        'user': user,
        'hr_profile': hr_profile,
        'jobs': jobs,
    }
    
    return render(request, 'admin_portal/view_hr_profile.html', context)


@login_required(login_url='login_user')
@admin_required
def view_candidate_profile(request, user_id):
    """View Candidate profile"""
    try:
        AdminUser.objects.get(user=request.user)
    except AdminUser.DoesNotExist:
        return HttpResponseForbidden('Admin access denied.')
    
    user = get_object_or_404(User, id=user_id)
    
    try:
        candidate_profile = CandidateProfile.objects.get(user=user)
    except CandidateProfile.DoesNotExist:
        candidate_profile = None
    
    # Get applications
    from hr.models import candidateApplication
    applications = candidateApplication.objects.filter(user=user)
    
    context = {
        'user': user,
        'candidate_profile': candidate_profile,
        'applications': applications,
    }
    
    return render(request, 'admin_portal/view_candidate_profile.html', context)


@login_required(login_url='login_user')
@admin_required
def admin_login(request):
    """Admin login page (redirects if already authenticated as admin)"""
    try:
        AdminUser.objects.get(user=request.user)
        return redirect('admin_dashboard')
    except AdminUser.DoesNotExist:
        pass
    
    messages.error(request, 'You do not have admin privileges.')
    return redirect('login_user')
