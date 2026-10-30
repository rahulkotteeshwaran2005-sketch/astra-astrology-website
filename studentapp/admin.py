from django.contrib import admin
from .models import Astrologer, Booking

@admin.register(Astrologer)
class AstrologerAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "price_per_minute", "is_online", "is_featured")
    list_filter = ("is_online", "is_featured")
    search_fields = ("name", "skills", "languages")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "astrologer", "preferred_date", "preferred_time", "status")
    list_filter = ("status", "consultation_type")
    search_fields = ("customer_name", "email", "astrologer__name")