from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hr.models import JobPost, ShortlistedCandidate, RecruiterProfile
from candidate.models import CandidateProfile, candidateApplication
from candidate.forms import JobApplicationForm, CandidateProfileForm
from .recommended import recommend_jobs_for_user
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User



@login_required(login_url='login_user')

# Display candidate dashboard with sidebar navigation and advanced filtering
def candidate_dashboard(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        profile = None
    
    search_query = request.GET.get('search', '')
    filter_by = request.GET.get('filter_by', 'keyword')
    location = request.GET.get('location', '')
    date_posted = request.GET.get('date_posted', '')
    min_salary = request.GET.get('min_salary', '')
    max_salary = request.GET.get('max_salary', '')
    sort_by = request.GET.get('sort_by', 'relevance')
    employment_type = request.GET.get('employment_type', '')
    work_mode = request.GET.get('work_mode', '')
    
    # Get all available jobs just kike select * from jobpost
    jobs = JobPost.objects.all()
    search_placeholder = 'Search jobs here...'
    

    # Apply filters based on dropdown selection  (note .filter is just like where clause in sql)
    #search qyery is user typed word in html box
    if filter_by == 'keyword' and search_query:
        jobs = jobs.filter(title__icontains=search_query)
        search_placeholder = 'Search jobs here...'
    elif filter_by == 'location' and search_query:
        jobs = jobs.filter(address__icontains=search_query)
        search_placeholder = 'Search by location...'
    elif filter_by == 'company' and search_query:
        jobs = jobs.filter(CompanyName__icontains=search_query)
        search_placeholder = 'Search by company name...'
    elif filter_by == 'date_24':
        cutoff_date = timezone.now() - timedelta(hours=24)
        jobs = jobs.filter(created_at__gte=cutoff_date)
        search_placeholder = 'Showing jobs from last 24 hours'
    elif filter_by == 'date_7':
        cutoff_date = timezone.now() - timedelta(days=7)
        jobs = jobs.filter(created_at__gte=cutoff_date)
        search_placeholder = 'Showing jobs from last 7 days'
    elif filter_by == 'date_30':
        cutoff_date = timezone.now() - timedelta(days=30)
        jobs = jobs.filter(created_at__gte=cutoff_date)
        search_placeholder = 'Showing jobs from last 30 days'
    elif filter_by == 'salary_high':
        jobs = jobs.order_by('-salaryHigh')
        search_placeholder = 'Sorted by highest salary'
    elif filter_by == 'salary_low':
        jobs = jobs.order_by('salaryLow')
        search_placeholder = 'Sorted by lowest salary'
    elif filter_by == 'newest':
        jobs = jobs.order_by('-created_at')
        search_placeholder = 'Showing newest jobs first'
    elif filter_by == 'employment_full':
        jobs = jobs.filter(employment_type='full-time')
        search_placeholder = 'Showing Full-time jobs'
    elif filter_by == 'employment_part':
        jobs = jobs.filter(employment_type='part-time')
        search_placeholder = 'Showing Part-time jobs'
    elif filter_by == 'employment_intern':
        jobs = jobs.filter(employment_type='internship')
        search_placeholder = 'Showing Internship jobs'
    elif filter_by == 'employment_contract':
        jobs = jobs.filter(employment_type='contract')
        search_placeholder = 'Showing Contract jobs'
    elif filter_by == 'employment_freelance':
        jobs = jobs.filter(employment_type='freelance')
        search_placeholder = 'Showing Freelance jobs'
    elif filter_by == 'work_onsite':
        jobs = jobs.filter(work_mode='on-site')
        search_placeholder = 'Showing On-site jobs'
    elif filter_by == 'work_remote':
        jobs = jobs.filter(work_mode='remote')
        search_placeholder = 'Showing Remote jobs'
    elif filter_by == 'work_hybrid':
        jobs = jobs.filter(work_mode='hybrid')
        search_placeholder = 'Showing Hybrid jobs'
    elif filter_by == 'salary_range' and min_salary and max_salary:
        try:
            min_val = float(min_salary)
            max_val = float(max_salary)
            jobs = jobs.filter(salaryLow__gte=min_val, salaryHigh__lte=max_val)
            search_placeholder = f'Salary range: {min_salary} - {max_salary}'
        except (ValueError, TypeError):
            pass
    
    # Legacy Location filter (for backward compatibility)
    if location:
        jobs = jobs.filter(address__icontains=location)
    
    # Legacy Date Posted filter
    if date_posted:
        try:
            days = int(date_posted)
            cutoff_date = timezone.now() - timedelta(days=days)
            jobs = jobs.filter(created_at__gte=cutoff_date)
        except (ValueError, TypeError):
            pass
    
    # Salary Range filters validation
    if min_salary and not filter_by.startswith('salary'):
        try:
            min_sal = float(min_salary)
            if min_sal < 0:
                min_sal = 0
            jobs = jobs.filter(salaryHigh__gte=min_sal)
        except (ValueError, TypeError):
            pass
    
    if max_salary and not filter_by.startswith('salary'):
        try:
            max_sal = float(max_salary)
            if max_sal <= 0:
                max_sal = 0
            jobs = jobs.filter(salaryLow__lte=max_sal)
        except (ValueError, TypeError):
            pass
    
    # Legacy Sort By (only if not already sorted by filter_by)
    if filter_by not in ['salary_high', 'salary_low', 'newest', 'salary_range']:
        if sort_by == 'newest':
            jobs = jobs.order_by('-created_at')
        elif sort_by == 'salary_high':
            jobs = jobs.order_by('-salaryHigh')
        elif sort_by == 'salary_low':
            jobs = jobs.order_by('salaryLow')
        else:  # Default sorting by relevance (could be based on search query or other factors)
            jobs = jobs.order_by('-created_at')
    
    applied_jobs = candidateApplication.objects.filter(user=request.user)
    applied_job_ids = [app.job.id for app in applied_jobs]
    
    # Create a mapping of job ID to application status for quick lookup
    job_status_map = {app.job.id: app.status for app in applied_jobs}
    
    # Attach application status to each job in the list
    for job in jobs:
        if job.id in job_status_map:
            job.application_status = job_status_map[job.id]
        else:
            job.application_status = None

    # Attach display status for jobs (Expired if expired, else application status)
    for job in jobs:
        if job.is_expired:
            job.display_status = "Expired"
        else:   
            job.display_status = job.application_status
    
    shortlisted_jobs = ShortlistedCandidate.objects.filter(candidate__user=request.user)
    shortlisted_count = shortlisted_jobs.count()
    
    # Show notification only for newly shortlisted candidates 
    newly_shortlisted = shortlisted_jobs.filter(notification_sent=False)
    for shortlist in newly_shortlisted:
        messages.info(request, f"Great news! You have been shortlisted for {shortlist.job.title}!")
        shortlist.notification_sent = True
        shortlist.save()
    
    context = {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'shortlisted_count': shortlisted_count,
        'profile': profile,
        'search_query': search_query,
        'filter_by': filter_by,
        'search_placeholder': search_placeholder,
        'location': location,
        'date_posted': date_posted,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'sort_by': sort_by,
        'employment_type': employment_type,
        'work_mode': work_mode,
    }
    return render(request, 'candidate/dashboard_with_nav.html', context)




#Application fillup and sumbitted
@login_required(login_url='login_user')
def job_detail(request, pk):
    job = JobPost.objects.get(id=pk)  # .firtst eturns the first object in the QuerySet or None if no record exists.
    application = candidateApplication.objects.filter(user=request.user, job=job).first()
    has_applied = application is not None
    application_status = application.status if application else None
    is_shortlisted = ShortlistedCandidate.objects.filter(candidate__user=request.user, job=job).exists()
    is_rejected = application_status == 'rejected' if application else False
    
    company_profile_exists = RecruiterProfile.objects.filter(user=job.user).exists()
    
    #Application submitted
    if request.method == 'POST':
        if job.is_expired:
            messages.error(request, "This job posting has expired. You cannot apply for expired jobs.")
        else:
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

    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'application_status': application_status,
        'is_shortlisted': is_shortlisted,
        'is_rejected': is_rejected,
        'form': form,
        'company_profile_exists': company_profile_exists,
    }
    return render(request, 'candidate/job_detail.html', context)




# Display jobs where candidate has been shortlisted
@login_required(login_url='login_user')
def shortlisted_jobs(request):
    shortlisted = ShortlistedCandidate.objects.filter(candidate__user=request.user).order_by('-shortlisted_at')
    
    context = {
        'shortlisted_jobs': shortlisted,
        'count': shortlisted.count(),
    }
    return render(request, 'candidate/shortlisted.html', context)




#Candidate Profile
@login_required(login_url='login_user')
def candidate_profile(request):
    #Display candidate profile creation/editing page
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile) #instance : update this existing profile instance
        if form.is_valid():
            profile = form.save(commit=False) #no permanant change so edit possible
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('candidate_profile')
        else:
            messages.error(request, "Please correct the errors below and resubmit the form.")
    else:
        form = CandidateProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'candidate/profile.html', context)



# Delete Candidate Profile
@login_required(login_url='login_user')
def delete_profile(request):

    try:
        profile = CandidateProfile.objects.get(user=request.user)
        profile.delete()
        messages.success(request, "Profile deleted successfully!")
    except CandidateProfile.DoesNotExist:
        messages.error(request, "No profile found to delete.")
    
    return redirect('candidate_profile')


# Display all applied jobs in application status
@login_required(login_url='login_user')
def applied_jobs(request):
    applications = candidateApplication.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_at')


    # Create a list with job and application status
    applied_jobs_list = []
    for app in applications:
        applied_jobs_list.append({
            'job': app.job,
            'application': app,
            'status': app.status,
            'applied_at': app.applied_at,
        })

    # Add red notifications for expired applied jobs
    for item in applied_jobs_list:
        if item['job'].is_expired:
            messages.error(request, f"The job '{item['job'].title}' has expired.")

    pending_count = applications.filter(status='pending').count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    selected_count = applications.filter(status='selected').count()
    rejected_count = applications.filter(status='rejected').count()

    context = {
        'applied_jobs': applied_jobs_list,
        'total_count': applications.count(),
        'pending_count': pending_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'candidate/applied_jobs.html', context)



#  Display HR/Company profile
@login_required(login_url='login_user')
def view_hr_profile(request, user_id):

    hr_user = get_object_or_404(User, id=user_id) # Retrieve the HR user with the given user_id , If no such user exists, return a 404 error page automatically.
    
    try:
        profile = RecruiterProfile.objects.get(user=hr_user)
    except RecruiterProfile.DoesNotExist:
        return render(request, '404.html', {'message': 'Company profile not found'}, status=404)
    
    context = {
        'profile': profile,
        'hr_user': hr_user,
    }
    return render(request, 'candidate/view_hr_profile.html', context)



# Show job recommendations for candidate using the Bag of Words (BoW) match with profile.
@login_required(login_url='login_user')
def recommended_jobs(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist: # Show message inside the Recommended Jobs page instead of redirecting
        context = {
            'profile': None,
            'recommendations': [],
            'missing_profile': True,
        }
        return render(request, 'candidate/recommended_jobs.html', context)

    scored_jobs = recommend_jobs_for_user(request.user, top_n=20) #limit upto 20

    # Extra safety: enforce the 0.25 threshold here as well
    recommendations = [
        {
            'job': job,
            'score': score,
        }
        for job, score in scored_jobs
        if score >= 0.25
    ]

    context = {
        'profile': profile,
        'recommendations': recommendations,
        'missing_profile': False,
    }
    return render(request, 'candidate/recommended_jobs.html', context)

