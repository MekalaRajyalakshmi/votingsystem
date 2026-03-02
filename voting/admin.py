from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Nominee


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'votes', 'image_tag')
    list_filter = ('category',)
    search_fields = ('name',)

    # Fields visible in the form when you click "Add" or "Edit"
    fields = ('name', 'category', 'image', 'votes')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;"/>', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'