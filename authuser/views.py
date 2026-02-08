from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from hr.models import hr
from candidate.models import CandidateAccount
from authuser.models import ContactMessage


def register_candidate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            msg = "Password didn't match"
            return render(request, 'authuser/candidateregister.html', {'msg': msg})
        if User.objects.filter(username=username).exists():
            msg = "User already Exists..."
            return render(request, 'authuser/candidateregister.html', {'msg': msg})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Create CandidateAccount for the new user
            CandidateAccount.objects.create(user=user, account_status='active')
            messages.success(request, 'Registration successful! Please log in with your credentials.')
            return redirect('login_user')
        except Exception as e:
            msg = "Registration failed. Please try again later."
            return render(request, 'authuser/candidateregister.html', {'msg': msg})
    
    return render(request, 'authuser/candidateregister.html')


def register_hr(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            msg = "Password didn't match"
            return render(request, 'authuser/hrregister.html', {'msg': msg})
        if User.objects.filter(username=username).exists():
            msg = "User already Exists..."
            return render(request, 'authuser/hrregister.html', {'msg': msg})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            hr.objects.create(user=user)
            messages.success(request, 'Registration successful! Please log in with your credentials.')
            return redirect('login_user')
        except Exception as e:
            msg = "Registration failed. Please try again later."
            return render(request, 'authuser/hrregister.html', {'msg': msg})
    
    return render(request, 'authuser/hrregister.html')


def login_user(request):
    msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            # Block superusers and staff from logging in on normal pages
            if user.is_superuser or user.is_staff:
                msg = "Superusers and staff members must log in through the admin panel."
                return render(request, 'authuser/loginUser.html', {'msg': msg})
            
            login(request, user)
            # Check if HR/Recruiter
            if hr.objects.filter(user=user).exists():
                return redirect('hrdash')
            else:
                return redirect('candidate_dashboard')
        else:
            msg = "Username and Password is not valid"

    return render(request, 'authuser/loginUser.html', {'msg': msg})


def logoutuser(request):
    logout(request)
    return redirect('login_user')


def contact_us(request):
    """Handle contact form submission and store messages in database"""
    msg = None
    if request.method == 'POST':
        name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validation
        if not name or not email or not message_text:
            msg = "All fields are required."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'error'})
        
        if len(name) < 2:
            msg = "Name must be at least 2 characters long."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'error'})
        
        if '@' not in email:
            msg = "Please enter a valid email address."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'error'})
        
        if len(message_text) < 10:
            msg = "Message must be at least 10 characters long."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'error'})
        
        try:
            # Save message to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )
            msg = "Your message has been sent successfully! We'll get back to you soon."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'success'})
        except Exception as e:
            msg = "An error occurred while sending your message. Please try again later."
            return render(request, 'hr/contactus.html', {'msg': msg, 'msg_type': 'error'})
    
    return render(request, 'hr/contactus.html')
