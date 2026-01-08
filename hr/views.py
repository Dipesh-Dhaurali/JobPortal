from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from hr.models import JobPost, candidateApplication, ShortlistedCandidate, SelectedCandidate
from hr.forms import JobPostForm
from candidate.models import CandidateProfile

def home(request):
    """View for the main landing page"""
    return render(request, 'hr/index.html')

def blog_detail(request, slug):
    """View for displaying individual blog/article content"""
    blogs = {
        'mastering-remote-interview': {
            'title': 'Mastering the Remote Interview',
            'category': 'CAREER ADVICE',
            'image': 'hr/images/blog-remote-interview.jpg',
            'content': """
                <p>In 2026, remote interviews have become the standard for the first round of recruitment. To stand out, you need more than just technical skills; you need to master the digital medium.</p>
                <h3>1. Perfect Your Technical Setup</h3>
                <p>Ensure your internet connection is stable and your audio is crystal clear. A high-quality microphone can make a significant difference in how professional you sound.</p>
                <h3>2. Master Your Background</h3>
                <p>Your background should be clean and professional. Avoid distractions. Good lighting is essential—natural light from the front is usually best.</p>
                <h3>3. Engage with the Camera</h3>
                <p>Look into the camera lens, not at the screen, to simulate eye contact. This small adjustment makes you appear much more engaged and confident.</p>
            """
        },
        'what-hr-looks-for-2026': {
            'title': 'What HR Looks for in 2026',
            'category': 'HIRING TRENDS',
            'image': 'hr/images/blog-hr-trends.jpg',
            'content': """
                <p>The job market is evolving rapidly. HR professionals are no longer just looking for specific degrees; they are looking for adaptability and specialized soft skills.</p>
                <h3>1. AI Literacy</h3>
                <p>Being able to work alongside AI tools is now a fundamental requirement across almost all industries. Demonstrate how you use technology to improve your efficiency.</p>
                <h3>2. Emotional Intelligence (EQ)</h3>
                <p>As technical tasks become more automated, the human element—empathy, leadership, and collaboration—becomes even more valuable.</p>
                <h3>3. Continuous Learning Mindset</h3>
                <p>Show that you are a self-starter who proactively seeks out new knowledge and stays ahead of industry trends.</p>
            """
        },
        'balancing-hustle-and-health': {
            'title': 'Balancing Hustle and Health',
            'category': 'LIFESTYLE',
            'image': 'hr/images/blog-work-life.jpg',
            'content': """
                <p>Climbing the corporate ladder shouldn't come at the cost of your mental and physical well-being. True success is sustainable.</p>
                <h3>1. Set Clear Boundaries</h3>
                <p>Define your working hours and stick to them. Avoid checking emails after your designated 'off' time to allow your brain to fully disconnect.</p>
                <h3>2. Prioritize Movement</h3>
                <p>Even a 15-minute walk during lunch can significantly boost your mood and cognitive function. Regular exercise is the best defense against burnout.</p>
                <h3>3. Practice Mindfulness</h3>
                <p>Taking moments throughout the day to breathe and center yourself can help manage stress and maintain focus during high-pressure situations.</p>
            """
        }
    }
    
    blog = blogs.get(slug)
    if not blog:
        return redirect('home')
        
    return render(request, 'hr/blog_detail.html', {'blog': blog})

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


@login_required(login_url='login_user')
def view_candidate_profile(request, user_id):
    """View a candidate's complete profile"""
    candidate_user = get_object_or_404(User, id=user_id)
    
    try:
        profile = CandidateProfile.objects.get(user=candidate_user)
    except CandidateProfile.DoesNotExist:
        messages.warning(request, f"Candidate {candidate_user.username} has not created a profile yet.")
        return redirect('hrdash')
    
    context = {
        'candidate_user': candidate_user,
        'profile': profile,
    }
    return render(request, 'hr/view_candidate_profile.html', context)
