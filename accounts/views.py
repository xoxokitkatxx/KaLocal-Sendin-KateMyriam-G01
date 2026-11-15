from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import KaLocalRegistrationForm, UserProfileUpdateForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = KaLocalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! Please log in with your credentials."
            )
            return redirect('login')
        else:
            messages.error(
                request,
                "Please correct the errors highlighted below."
            )
    else:
        form = KaLocalRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.profile.full_name}!")
            return redirect('dashboard_redirect')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('login')


@login_required
def dashboard_redirect(request):
    """Routes the logged-in user to their role-specific dashboard."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact the administrator.")
        logout(request)
        return redirect('login')

    if profile.role == UserProfile.ROLE_VENDOR:
        return redirect('vendor_dashboard')
    return redirect('consumer_dashboard')


@login_required
def vendor_dashboard(request):
    """Vendor-only dashboard. Blocks Consumers from accessing this URL."""
    profile = request.user.profile
    if profile.role != UserProfile.ROLE_VENDOR:
        messages.error(
            request,
            "Access Denied: Consumers are not authorized to view the Vendor Dashboard."
        )
        return redirect('consumer_dashboard')

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/vendor_dashboard.html', context)


@login_required
def consumer_dashboard(request):
    """Consumer-only dashboard. Blocks Vendors from accessing this URL."""
    profile = request.user.profile
    if profile.role != UserProfile.ROLE_CONSUMER:
        messages.error(
            request,
            "Access Denied: Vendors are not authorized to view the Consumer Dashboard."
        )
        return redirect('vendor_dashboard')

    # Fetch active vendors in the consumer's barangay for the directory preview
    local_vendors = UserProfile.objects.filter(
        role=UserProfile.ROLE_VENDOR,
        location=profile.location
    )

    context = {
        'profile': profile,
        'local_vendors': local_vendors,
    }
    return render(request, 'accounts/consumer_dashboard.html', context)


@login_required
def profile_view(request):
    """Displays the logged-in user's own profile information."""
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})


@login_required
def profile_edit(request):
    """Allows the logged-in user to update only their own profile."""
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileUpdateForm(
            request.POST,
            instance=profile,
            user_instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below to update your profile.")
    else:
        form = UserProfileUpdateForm(
            instance=profile,
            user_instance=request.user
        )

    return render(request, 'accounts/profile_edit.html', {'form': form, 'profile': profile})