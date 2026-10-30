from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Astrologer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    title = models.CharField(max_length=120, blank=True)
    skills = models.CharField(max_length=250, help_text="Comma-separated skills")
    languages = models.CharField(max_length=150, help_text="Comma-separated languages")
    experience = models.PositiveIntegerField(default=1)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    review_count = models.PositiveIntegerField(default=0)
    price_per_minute = models.PositiveIntegerField(default=30)
    image_url = models.URLField(blank=True)
    about = models.TextField(blank=True)
    is_online = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_featured", "-rating", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "astrologer"
            slug, n = base, 1
            while Astrologer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def skill_list(self):
        return [x.strip() for x in self.skills.split(",") if x.strip()]

    @property
    def language_list(self):
        return [x.strip() for x in self.languages.split(",") if x.strip()]


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True
    )
    astrologer = models.ForeignKey(Astrologer, on_delete=models.PROTECT, related_name="bookings")
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    consultation_type = models.CharField(max_length=10, choices=[("Chat", "Chat"), ("Call", "Call")], default="Chat")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    question = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[("Pending","Pending"),("Confirmed","Confirmed"),("Completed","Completed"),("Cancelled","Cancelled")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.astrologer.name}"