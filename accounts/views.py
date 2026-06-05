import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/register.html')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── AJAX: Register ───────────────────────────────────────────
@require_POST
def ajax_register(request):
    try:
        data = json.loads(request.body)
        email    = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not email or not username or not password:
            return JsonResponse({'success': False, 'error': 'All fields are required.'})

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered.'})

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already taken.'})

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            provider='local'
        )
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'success': True, 'redirect': '/dashboard/'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@require_POST
def ajax_login(request):
    try:
        data = json.loads(request.body)
        email    = data.get('email', '').strip().lower()
        password = data.get('password', '')

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid email or password.'})

        # Authenticate using username (ModelBackend requires username)
        user = authenticate(request, username=user_obj.username, password=password)

        # Fallback: check password directly
        if user is None and user_obj.check_password(password):
            user = user_obj

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'success': True, 'redirect': '/dashboard/'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid email or password.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@staff_member_required
def users_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    total = users.count()
    return render(request, 'accounts/users_list.html', {'users': users, 'total': total})

@staff_member_required
def user_detail(request, pk):
    user = CustomUser.objects.get(pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})