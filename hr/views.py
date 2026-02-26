from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from hr.models import JobPost, ShortlistedCandidate, SelectedCandidate, RecruiterProfile
from hr.forms import JobPostForm, HRProfileForm
from candidate.models import CandidateProfile, candidateApplication
from authuser.models import ContactMessage
from django.db.models import Q
from django.utils.safestring import mark_safe
from hr.smsSystem import send_hr_action_email, send_contact_form_email



#  Display HR profile creation/editing page
@login_required(login_url='login_user')
def hr_profile(request):
    try:
        profile = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = HRProfileForm(request.POST, request.FILES, instance=profile) #instance : update this existing profile instance
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile saved successfully!")
            return redirect('hr_profile')
    else:
        form = HRProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'navbar_title': 'Build your profile',
    }
    return render(request, 'hr/profile.html', context)



# Delete HR Profile
@login_required(login_url='login_user')
def delete_hr_profile(request):
    try:
        profile = RecruiterProfile.objects.get(user=request.user)
        profile.delete()
        messages.success(request, "Profile deleted successfully!")
    except RecruiterProfile.DoesNotExist:
        messages.error(request, "No profile found to delete.")
    
    return redirect('hr_profile')


# View for the main landing page
def home(request):
    return render(request, 'hr/index.html')


# View for the About Us page
def about_us(request):
    return render(request, 'hr/aboutus.html')


# View for displaying individual blog/article content
def blog_detail(request, slug):
    
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
        },


        'top-tips-landing-dream-job': {
            'title': 'Top Tips for Landing Your Dream Job',
            'category': 'JOB SEARCH',
            'image': 'hr/images/blog-job-search-tips.jpg',
            'content': """
                <p>Finding and landing your dream job requires more than just sending out resumes. In today's competitive job market, you need a strategic approach and proven techniques to stand out from other candidates.</p>
                <h3>1. Tailor Your Resume for Each Position</h3>
                <p>Generic resumes rarely make an impact. Study the job description carefully and highlight the skills and experiences most relevant to the role. Use keywords from the job posting to pass through automated screening systems.</p>
                <h3>2. Build a Strong Professional Network</h3>
                <p>Many positions are filled through referrals before they're even posted publicly. Attend industry events, connect with professionals on LinkedIn, and maintain relationships with former colleagues. A personal introduction can significantly increase your chances.</p>
                <h3>3. Prepare Thoroughly for Interviews</h3>
                <p>Research the company deeply—understand their mission, recent news, and culture. Prepare specific examples of your accomplishments using the STAR method (Situation, Task, Action, Result). Practice your answers but keep them conversational and authentic.</p>
                <h3>4. Follow Up Strategically</h3>
                <p>After your interview, send a thoughtful thank-you email within 24 hours. Reference specific conversations you had and reiterate your genuine interest in the position. This demonstrates professionalism and keeps you fresh in their mind.</p>
                <h3>5. Don't Stop at "No"</h3>
                <p>Rejection is part of the process. Instead of getting discouraged, ask for feedback on what you could improve. Many candidates land positions with companies that initially rejected them because they persisted professionally.</p>
            """
        }
    }
    

    blog = blogs.get(slug) # Fetches exactly one object whose slug matches the value of slug.
    if not blog:
        return redirect('home')
        
    return render(request, 'hr/blog_detail.html', {'blog': blog})



#HR homepage / hrdashboard
@login_required(login_url='login_user')
def hrhome(request):
    jobs = JobPost.objects.filter(user=request.user).order_by('-created_at')
    
    search_query = request.GET.get('search', '').strip()
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)
    
    context = {
        'jobs': jobs,
        'search_query': search_query,
        'navbar_title': 'Welcome to HR Job Portal'  
    }
    return render(request, 'hr/hrdashboard.html', context)



# Job post page
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
    else:
        form = JobPostForm()
    
    context = {
        'form': form,
        'navbar_title': 'Post New Job Here'  
    }
    return render(request, 'hr/postjob.html', context)



# Edit job in dashboard
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




# Delete a post job
@login_required(login_url='login_user')
def delete_job(request, pk):
    job = get_object_or_404(JobPost, id=pk, user=request.user)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('hrdash')
    
    context = {'job': job}
    return render(request, 'hr/deletejob.html', context)




# candidate details (button inside)
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
        'navbar_title': 'View Candidate Application',
    }
    return render(request, 'hr/candidate.html', context)




# Shortlist a candidate for a job
@login_required(login_url='login_user')
@require_http_methods(["POST"])
def select_candidate(request, pk):
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:  # Checks whether the current user is the owner of the job if not no action
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')

    application.status = 'shortlisted'
    application.save()

    if not ShortlistedCandidate.objects.filter(candidate=application).exists(): #Prevents duplicate shortlisting.
        ShortlistedCandidate.objects.create(
            job=application.job,
            candidate=application,
            notification_sent=True
        )

    # Send email notification (handle success/failure gracefully)
    candidate_user = application.user
    email_success, email_message = send_hr_action_email(application, 'shortlisted')
    
    messages.success(request, f"Candidate {candidate_user.username} shortlisted successfully!")
    
    if email_success:
        messages.success(request, f"✓ Notification email sent to {candidate_user.email}")
    else:
        messages.warning(request, f"⚠ Email notification failed: {email_message}")

    return redirect('candidate_details', pk=application.job.id)





# select final candidate  Select (accept) a shortlisted candidate for the job
@login_required(login_url='login_user')
@require_http_methods(["POST"])
def select_final_candidate(request, pk):
    
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

    # Send email notification (handle success/failure gracefully)
    candidate_user = application.user
    email_success, email_message = send_hr_action_email(application, 'selected')

    messages.success(request, f"Candidate {candidate_user.username} selected successfully!")
    
    if email_success:
        messages.success(request, f"✓ Selection email sent to {candidate_user.email}")
    else:
        messages.warning(request, f"⚠ Email notification failed: {email_message}")
    
    return redirect('candidate_details', pk=application.job.id)





#  Reject a candidate for a job
@login_required(login_url='login_user')
@require_http_methods(["POST"])
def reject_candidate(request, pk):
   
    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')
    
    application.status = 'rejected'
    application.save()
    
    # Send email notification (handle success/failure gracefully)
    candidate_user = application.user
    email_success, email_message = send_hr_action_email(application, 'rejected')

    messages.success(request, f"Candidate {candidate_user.username} rejected successfully!")
    
    if email_success:
        messages.info(request, f"✓ Rejection email sent to {candidate_user.email}")
    else:
        messages.warning(request, f"⚠ Email notification failed: {email_message}")
    return redirect('candidate_details', pk=application.job.id)




# Reject a shortlisted candidate
@login_required(login_url='login_user')
@require_http_methods(["POST"])
def reject_from_shortlist(request, pk):

    application = get_object_or_404(candidateApplication, id=pk)
    if application.job.user != request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('hrdash')

    application.status = 'rejected'
    application.save()

    # Send email notification (handle success/failure gracefully)
    candidate_user = application.user
    email_success, email_message = send_hr_action_email(application, 'rejected_after_shortlist')

    messages.success(request, f"Candidate {candidate_user.username} rejected from shortlist successfully!")
    
    if email_success:
        messages.info(request, f"✓ Rejection email sent to {candidate_user.email}")
    else:
        messages.warning(request, f"⚠ Email notification failed: {email_message}")
    
    return redirect('candidate_details', pk=application.job.id)




# View a candidate's profile
@login_required(login_url='login_user')
def view_candidate_profile(request, user_id):
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




# View all job history i.e posts and applications with advanced filtering
@login_required(login_url='login_user')
def job_history(request):
    all_jobs = JobPost.objects.filter(user=request.user).order_by('-created_at')
    
    display_mode = request.GET.get('mode', 'applications')
    
    all_applications = candidateApplication.objects.filter(
        job__user=request.user
    ).select_related('user', 'job').order_by('-applied_at')
    
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        all_applications = all_applications.filter(status=status_filter)
    
    search_query = request.GET.get('search', '').strip()
    if search_query:
        all_applications = all_applications.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(job__title__icontains=search_query)
        )
    
    total_applications = candidateApplication.objects.filter(job__user=request.user).count()
    pending_count = candidateApplication.objects.filter(
        job__user=request.user, status='pending'
    ).count()
    shortlisted_count = candidateApplication.objects.filter(
        job__user=request.user, status='shortlisted'
    ).count()
    selected_count = candidateApplication.objects.filter(
        job__user=request.user, status='selected'
    ).count()
    rejected_count = candidateApplication.objects.filter(
        job__user=request.user, status='rejected'
    ).count()
    
    context = {
        'all_jobs': all_jobs,
        'all_applications': all_applications,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'total_jobs': all_jobs.count(),
        'display_mode': display_mode,
        'navbar_title': mark_safe("""
        <h2><i class="fas fa-history"></i> Job History & Analytics</h2>
    """)
    }
    return render(request, 'hr/job_history.html', context)




# Handle contact form submission and store messages in database
def contact_us(request):
    msg = None
    msg_type = None

    if request.method == 'POST':
        print("[DEBUG] Contact form POST received")
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        print(f"[DEBUG] Form data - Name: {name}, Email: {email}, Message: {message_text[:50]}")

        if not name or not email or not message_text:
            msg = "All fields are required."
            msg_type = "error"
        else:
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    message=message_text
                )
                print("[DEBUG] Message saved successfully to database")

                # Send email notification
                email_success, email_message = send_contact_form_email(name, email, message_text)

                if email_success:
                    msg = "Thank you for contacting us. We will get back to you soon."
                    msg_type = "success"
                else:
                    msg = "Message received! Email notification failed, but we have your message."
                    msg_type = "warning"
            except Exception as e:
                print(f"[DEBUG] Error saving message: {e}")
                msg = f"Error saving message: {e}"
                msg_type = "error"

    return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': msg_type})
