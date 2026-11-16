from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Location, Product
from .forms import KaLocalRegistrationForm, UserProfileUpdateForm


def _get_or_create_user_profile(user):
    """Helper to safely fetch or create a profile (e.g., for superusers)."""
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        default_location = Location.objects.first()
        if not default_location:
            default_location, _ = Location.objects.get_or_create(
                barangay_name='Apas',
                defaults={'city': 'Cebu City'}
            )
        return UserProfile.objects.create(
            user=user,
            full_name=user.username,
            email=user.email or f"{user.username}@kalocal.local",
            role=UserProfile.ROLE_CONSUMER,
            location=default_location,
        )


@login_required
def dashboard_view(request):
    profile = _get_or_create_user_profile(request.user)

    if profile.role == UserProfile.ROLE_VENDOR:
        products = Product.objects.filter(vendor=profile)
        return render(request, 'accounts/vendor_dashboard.html', {
            'profile': profile,
            'products': products,
            'active_products_count': products.filter(is_active=True).count(),
        })

    barangays = Location.objects.all()
    selected_location = profile.location
    location_id = request.GET.get('location')
    if location_id and location_id.isdecimal():
        selected_location = Location.objects.filter(pk=location_id).first() or profile.location

    products = Product.objects.filter(
        vendor__location=selected_location,
        is_active=True,
    ).select_related('vendor', 'vendor__location')
    return render(request, 'accounts/consumer_dashboard.html', {
        'profile': profile,
        'barangays': barangays,
        'selected_location': selected_location,
        'products': products,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = KaLocalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to KaLocal! Your account has been created.")
            return redirect('dashboard')
    else:
        form = KaLocalRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_superuser:
                return redirect('admin:index')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    profile = _get_or_create_user_profile(request.user)

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
        form = UserProfileUpdateForm(
            instance=profile,
            user_instance=request.user
        )

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form,
    })


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your KaLocal account has been permanently deleted.")
        return redirect('login')
    return redirect('profile')