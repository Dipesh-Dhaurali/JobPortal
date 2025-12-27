from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from hr.models import JobPost, candidateApplication, ShortlistedCandidate, SelectedCandidate
from hr.forms import JobPostForm

@login_required(login_url='login_user')
def hrhome(request):
    # Get all jobs posted by this HR
    jobs = JobPost.objects.filter(user=request.user).order_by('-created_at')
    context = {'jobs': jobs}
    return render(request, 'hr/hrdashboard.html', context)


@login_required(login_url='login_user')
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('hrdash')
        # Form errors will now be displayed directly in the template
    else:
        form = JobPostForm()
    
    context = {'form': form}
    return render(request, 'hr/postjob.html', context)


@login_required(login_url='login_user')
def edit_job(request, pk):
    job = get_object_or_404(JobPost, id=pk, user=request.user)
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('hrdash')
    else:
        form = JobPostForm(instance=job)
    
    context = {
        'job': job,
        'form': form
    }
    return render(request, 'hr/editjob.html', context)


@login_required(login_url='login_user')
def delete_job(request, pk):
    job = get_object_or_404(JobPost, id=pk, user=request.user)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('hrdash')
    
    context = {'job': job}
    return render(request, 'hr/deletejob.html', context)


@login_required(login_url='login_user')
def candidate_details(request, pk):
    job = get_object_or_404(JobPost, id=pk, user=request.user)
    applications = candidateApplication.objects.filter(job=job).order_by('-applied_at')
    
    context = {
        'job': job,
        'applications': applications,
        'total_applications': applications.count(),
        'shortlisted_count': applications.filter(status='shortlisted').count(),
        'rejected_count': applications.filter(status='rejected').count(),
        'pending_count': applications.filter(status='pending').count(),
    }
    return render(request, 'hr/candidate.html', context)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def select_candidate(request, pk):
    """Shortlist a candidate for a job"""
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')
    
    application.status = 'shortlisted'
    application.save()
    
    if not ShortlistedCandidate.objects.filter(candidate=application).exists():
        ShortlistedCandidate.objects.create(
            job=application.job,
            candidate=application,
            notification_sent=True
        )
    
    candidate_user = application.user
    messages.success(request, f"Candidate {candidate_user.username} shortlisted successfully!")
    messages.info(request, f"Notification sent to {candidate_user.username}")
    
    return redirect('candidate_details', pk=application.job.id)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def reject_candidate(request, pk):
    """Reject a candidate for a job"""
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')
    
    application.status = 'rejected'
    application.save()
    
    messages.success(request, f"Candidate {application.user.username} rejected successfully!")
    return redirect('candidate_details', pk=application.job.id)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def select_final_candidate(request, pk):
    """Select (accept) a shortlisted candidate for the job"""
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')
    
    application.status = 'selected'
    application.save()
    
    if not SelectedCandidate.objects.filter(candidate=application).exists():
        SelectedCandidate.objects.create(
            job=application.job,
            candidate=application
        )
    
    messages.success(request, f"Candidate {application.user.username} selected successfully!")
    return redirect('candidate_details', pk=application.job.id)


@login_required(login_url='login_user')
@require_http_methods(["POST"])
def reject_from_shortlist(request, pk):
    """Reject a shortlisted candidate"""
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')
    
    application.status = 'rejected'
    application.save()
    
    messages.success(request, f"Candidate {application.user.username} rejected successfully!")
    return redirect('candidate_details', pk=application.job.id)
