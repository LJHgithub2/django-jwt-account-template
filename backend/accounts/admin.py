# accounts/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user_email",
        "gender",
        "age_display",
        "profile_thumb",
        "phone_number",
        "edit_in_user_button",  # ✅ User 변경 화면으로 가는 버튼
    )
    list_select_related = ("user",)
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "phone_number")
    list_filter = ("gender",)
    ordering = ("user__username",)
    list_per_page = 50

    fieldsets = (
        ("사용자", {"fields": ("user",)}),
        ("기본 정보", {"fields": ("gender", "birth_date", "phone_number")}),
        ("프로필", {"fields": ("bio", "profile_picture", "image_preview")}),
        ("읽기 전용", {"fields": ("age_display",)}),
    )
    readonly_fields = ("image_preview", "age_display")
    autocomplete_fields = ("user",)

    @admin.display(description="Full Name")
    def full_name(self, obj):
        parts = [obj.user.first_name or "", obj.user.last_name or ""]
        return " ".join(p for p in parts if p).strip() or "-"

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email or "-"

    @admin.display(description="Age")
    def age_display(self, obj):
        return obj.age if obj.age is not None else "-"

    @admin.display(description="Profile Picture")
    def profile_thumb(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="44" height="44" style="object-fit:cover;border-radius:50%;" />',
                obj.profile_picture.url
            )
        return "—"

    @admin.display(description="Image Preview")
    def image_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-width:240px; height:auto; border-radius:8px;" />',
                obj.profile_picture.url
            )
        return "No Image"

    @admin.display(description="Edit in User")
    def edit_in_user_button(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user_id])
        return format_html('<a class="button" href="{}">User에서 편집</a>', url)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")
