from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from hr.models import hr
from candidate.models import CandidateAccount


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
