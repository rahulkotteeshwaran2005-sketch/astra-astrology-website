from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Astrologer, Booking

def home(request):
    featured = Astrologer.objects.filter(is_featured=True)[:4]
    if not featured.exists():
        featured = Astrologer.objects.all()[:4]
    return render(request, "studentapp/index.html", {
        "featured_astrologers": featured,
        "astrologer_count": Astrologer.objects.count(),
    })

def astrologers(request):
    qs = Astrologer.objects.all()
    search = request.GET.get("q", "").strip()
    skill = request.GET.get("skill", "").strip()
    availability = request.GET.get("availability", "")
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(skills__icontains=search) |
                       Q(languages__icontains=search) | Q(title__icontains=search))
    if skill:
        qs = qs.filter(skills__icontains=skill)
    if availability == "online":
        qs = qs.filter(is_online=True)
    page_obj = Paginator(qs, 9).get_page(request.GET.get("page"))
    return render(request, "studentapp/astrologers.html", {
        "page_obj": page_obj, "search": search,
        "selected_skill": skill, "availability": availability,
    })

def profile(request, slug):
    item = get_object_or_404(Astrologer, slug=slug)
    return render(request, "studentapp/profile.html", {"astrologer": item})

def booking(request, slug):
    item = get_object_or_404(Astrologer, slug=slug)
    if request.method == "POST":
        try:
            date_value = timezone.datetime.strptime(request.POST.get("preferred_date", ""), "%Y-%m-%d").date()
            time_value = timezone.datetime.strptime(request.POST.get("preferred_time", ""), "%H:%M").time()
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid date and time.")
            return render(request, "studentapp/booking.html", {"astrologer": item})
        if date_value < timezone.localdate():
            messages.error(request, "Please choose today or a future date.")
            return render(request, "studentapp/booking.html", {"astrologer": item})
        Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            astrologer=item,
            customer_name=request.POST.get("customer_name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            consultation_type=request.POST.get("consultation_type", "Chat"),
            preferred_date=date_value, preferred_time=time_value,
            question=request.POST.get("question", "").strip(),
        )
        messages.success(request, "Your consultation request has been submitted.")
        return redirect("studentapp:booking_success")
    return render(request, "studentapp/booking.html", {"astrologer": item})

def booking_success(request):
    return render(request, "studentapp/booking_success.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("studentapp:home")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )

        if user is not None:
            login(request, user)
            return redirect(
                request.GET.get("next") or "studentapp:home"
            )

        messages.error(request, "Username or password is incorrect.")
        return redirect("studentapp:login")

    return render(
        request,
        "studentapp/login.html",
        {"next": request.GET.get("next", "")}
    )
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("studentapp:home")